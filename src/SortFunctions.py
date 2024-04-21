import os
import re
import pandas as pd
from Place import Place
from WriteToExcel import *
from Config import *

def start_row(df, list_of_names):
    for names in list_of_names:
        list = df.index[df.iloc[:, 0] == names].tolist()
        if len(list) > 0:
            return list[0] + 1
    return -1

def getDataFrames(path):
    df = pd.read_excel(path)

    start = start_row(df, ["Datum"])    # Find the row where the data starts
    # Create a new DataFrame without the first n rows
    data = df.iloc[start:].copy()
    data.rename(columns=df.iloc[start-1], inplace=True)
    print(data)
    data.dropna(how='all', inplace=True)
    
    data['Läkare'] = df.iloc[0,1]
    #data['Momsbelopp (kr)'] = ''
    print(data)
    return data

def format_number(number_str):
    number = int(number_str)
    formatted_number = '{:,.0f}'.format(number).replace(",", " ")
    return str(formatted_number)

def valid_time(time):
    char = ['.', ':']
    if numberOfDigits(time) == 6 and ':' in str(time) and time[6] == '0' and time[7] == '0' and time[5] == time[2]:
        return True
    if len(time) == 4 and numberOfDigits(time) == 4:
        if int(time[0]) == 2 and int(time[1]) < 4 and int(time[2]) < 6:
            return True
        elif int(time[0]) < 2 and int(time[1]) <= 9 and int(time[2]) < 6:
            return True        
    elif numberOfDigits(time) == 4 and len(time) == 5 and str(time[2]) in char:
        if int(time[0]) == 2 and int(time[1]) < 4 and int(time[3]) < 6:
            return True
        elif int(time[0]) < 2 and int(time[1]) <= 9 and int(time[3]) < 6:
            return True
    elif numberOfDigits(time) == 3 and len(time) == 4 and str(time[1]) in char:
        if int(time[0]) <= 9 and int(time[2]) < 6 and int(time[3]) <= 9:
            return True
    return False

def valid_date(date_str):

    # if (numberOfDigits(date_str) > 8):
    #     return False

    if (numberOfDigits(date_str) != 8) and (numberOfDigits(date_str) != 6) or len(date_str) != numberOfDigits(date_str):
        return False

    if len(date_str) == 8 and str(date_str)[0] == '2' and str(date_str)[1] == '0':
        date_str = str(date_str)[2:]
    if len(str(date_str)) == 1 and numberOfDigits(str(date_str)) == 1 and float(date_str) < 1 and float(date_str) > 0:
        return True
    if (numberOfDigits(date_str) != 6):
        return False
    if date_str.lower() == '':
        return False
    if date_str[5] == '0' and date_str[4] == '0':
        return False
    if date_str[2] == '0' and str(date_str)[3] == '0':
        return False
    return True

def missing_first_digit(time_str):  # checks if the first digit is missing in time-string
    patternA = r'^([0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'    
    patternB = r'^([0-9]|1[0-9]|2[0-3]).[0-5][0-9]$'    

    return re.match(patternA, time_str) or re.match(patternB, time_str)
    
def format_time(time_str):
    if len(time_str) == 4 and numberOfDigits(time_str) == 4:
        return time_str[0:2] + ':' + time_str[2:]
    elif len(time_str) == 4:
        return '0' + time_str[0] + ':' + time_str[2:]
    elif len(time_str) == 5: 
        return time_str[:2] + ':' + time_str[3:]
    
    if numberOfDigits(time_str) != 4:
        return str(time_str)[:5]
    

def numberOfDigits(personnummer):
    count = 0
    for char in str(personnummer):
        if char.isdigit():
            count += 1
    return count

def extract_digits(personnummer):
    digits_only = ''.join(filter(str.isdigit, personnummer))
    return digits_only

def personnummer(personnummer):

    personnummer = extract_digits(personnummer)

    if numberOfDigits(personnummer) == 6 or numberOfDigits(personnummer) == 8:
        return personnummer
    elif numberOfDigits(personnummer) == 12:
        return personnummer[:8]
    elif numberOfDigits(personnummer) == 10:
        return personnummer[:6]
    else:
        return 'okänd'

def fixNbr(nbr, char):          # removes space " ", and all characters that are not digits
    str(nbr.replace(" ", ""))
    nbr = ''.join(char for char in nbr if char.isdigit())
    return nbr + char

def modifyRow(row):
    row = row[columns_to_keep].copy()
    row['Distrikt'] = row['Distrikt'].lower().capitalize().replace(" ", "")
    if contains_kvv(str(row['Distrikt']).lower()):
        row['Tjänst'] = 'Jourläkare'
        district = 'krim'
    else:
        row['Tjänst'] = taskMapping[row['Tjänst'].lower().replace(" ", "")]
        district = placeMapping[row['Distrikt'].lower()].lower().replace(" ", "")
    row['Tid'] = format_time(str(row['Tid'])).replace(" ", "")
    op = taskMapping[row['Tjänst'].lower()]
    row['Kostnad'] = str(price_place_task[district][op]).replace(" ", "")
    row['Resor (kostnad)'] = fixNbr(str(row['Resor (kostnad)']), ' kr')
    row['Resor (km)'] = fixNbr(str(row['Resor (km)']), ' km')
    row['Momsbelopp (kr)'] = str(price_place_task[district][op] * 0.25).replace(" ", "")
    row['Datum'] = get_six_number_date(str(row['Datum']))
    row['Moms'] = '25 %'
    row['Pers.nr.'] = personnummer(str(row['Pers.nr.']))
    
    if row['Kostnad'] != '?':
        row['Kostnad'] = str(row['Kostnad']) + ' kr'
    addTime(row)
    return row


def get_six_number_date(date):
    if len(str(date)) == 8:
        return str(date)[2:]
    else:
        return date

def getDistance(row, col):
    if row[col] == '':
        return ''
    else:return fixNbr(str(row[col]), ' km')

def getCost(col, district, op, row):
    if row[col] == '':
        return ''
    elif row[col] == '?':
        return '?'
    else:
        return str(price_place_task[district][op]).replace(" ", "")

def addTime(row):
    if row['Tjänst'] == 'Blod':
        count = 0
        

def copyRow_exact(data, i):
    row = data.iloc[i].copy()
    return row

def valid_place(place):
    if place == '':
        return False
    for p in places:
        if place in p.aliases:
            return True
    return False

def valid_row(row):
    if (isinstance(row, int) or isinstance(row, str)) or str(row['Distrikt']).lower() == "":
        return False
    if not valid_place(str(row['Distrikt']).lower()) and not contains_kvv(str(row['Distrikt']).lower()):
        return False
    if not valid_time(str(row['Tid'])):
        return False
    if str(row['Tjänst']).lower().replace(" ", "") not in taskMapping:
        return False
    if numberOfDigits(str(row['Pers.nr.'])) != 4 and numberOfDigits(str(row['Pers.nr.'])) != 6 and numberOfDigits(str(row['Pers.nr.'])) != 10 and numberOfDigits(str(row['Pers.nr.'])) != 0 and numberOfDigits(str(row['Pers.nr.'])) != 8 and numberOfDigits(str(row['Pers.nr.'])) != 12:
        return False
    if not valid_date(str(row['Datum'])):
        return False
    return True

def contains_kvv(s):
    # Iterate through the string
    for i in range(len(s) - 2):  # Stop 2 characters before the end
        # Check if the current substring matches "lvv"
        if s[i:i+3].lower() == "kvv":
            return True
    for i in range(len(s) - 3):
        if s[i:i+3].lower() == "krim":
            return True
    return False

#8 col
def sort_data_between_districts(map, df):
    for i in range(df.shape[0]):    #iterate map with regular places
        row = copyRow_exact(df, i)
        added = False

        if not valid_row(row) or row.empty:
            map[misnamed].loc[len(map[misnamed].reset_index(drop=True))] = row
            continue

        for place in map:
            site = str(row.loc['Distrikt']).lower()
            if contains_kvv(site):
                map[krim].loc[len(map[krim].reset_index(drop=True))] = modifyRow(row)
                added = True
                break
            elif site in place.aliases:
                map[place].loc[len(map[place].reset_index(drop=True))] = modifyRow(row)
                added = True
                break
        if not added:
            map[misnamed].loc[len(map[misnamed].reset_index(drop=True))] = row
    return map

def getDistrictData(name, map):
    for place in map:
        if name in place.aliases:
            return map[place]

def sameColumns(col1, col2):
    for i in range(len(col1)-2):
        if col1[i] != col2[i]:
            return False
    return True

def run(path, map, runProgram):
    data = getDataFrames(path)
    if not sameColumns(data.columns, required_columns):
        return path.split("/")[-1]
    if not runProgram:
        return ""
    sort_data_between_districts(map, data)
    return ""

def iterate_folders(folder_path, target_folder):
    map = {}
    filesWithWrongFormat = []
    runProgram = True
    for place in places:
        map[place] = pd.DataFrame(columns=columns_to_keep)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and (filename.endswith('.xls') or filename.endswith('.xlsx')):
            success = run(file_path, map, runProgram)
            if success != "":
                filesWithWrongFormat.append(success)
                runProgram = False
    #if runProgram:
    for place in places:
        outputPath = target_folder + "/" + str(place)
        print(place)
        print(map[place])
        write(outputPath, map[place], place)
    return filesWithWrongFormat


iterate_folders("/Users/victorpekkari/Downloads/test", "testar90")

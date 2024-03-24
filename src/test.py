import os
import re
import time
import pandas as pd
from Place import Place
from WriteToExcel import *
from Constants import *

def start_row(df, list_of_names):
    for names in list_of_names:
        list = df.index[df.iloc[:, 0] == names].tolist()
        if len(list) > 0:
            return list[0] + 1
    return -1

def getDataFrames(path):
    df = pd.read_excel(path)

    start = start_row(df, ["Datum"])
    krimvard = start_row(df, ["Kriminalvården", "KVV", "kvv", "kriminalvården"])
    # Create a new DataFrame without the first n rows
    data = df.iloc[start:].copy()
    data.rename(columns=df.iloc[start-1], inplace=True)
    data.dropna(subset=[data.columns[1]], inplace=True)

    krim = df.iloc[krimvard:].copy()
    krim.rename(columns=df.iloc[start-1], inplace=True)
    krim.dropna(subset=[krim.columns[1]], inplace=True)

    return data, krim

def format_number(number_str):
    number = int(number_str)
    formatted_number = '{:,.0f}'.format(number).replace(",", " ")
    return str(formatted_number)

def is_valid_time_format(time):
    char = ['.', ':']
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
    if (numberOfDigits(date_str) != 6):
        return False
    if date_str.lower() == '':
        return False
    if date_str[5] == '0' and date_str[4] == '0':
        return False
    if date_str[2] == '0' and str(date_str)[3] == '0':
        return False

    return True

def missing_first_digit(time_str):
    # Define a regular expression pattern for the format h:mm
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
    
    #return is_valid_time_format(time_str, ':') or is_valid_time_format(time_str, '.') or missing_first_digit(time_str) or numberOfDigits(time_str) == 4

def numberOfDigits(personnummer):
    count = 0
    for char in str(personnummer):
        if char.isdigit():
            count += 1
    return count

def personnummer(personnummer):
    if numberOfDigits(personnummer) == 4:
        return 'xxxxxx-' + personnummer
    elif numberOfDigits(personnummer) == 6:
        return personnummer + '-xxxx'
    elif numberOfDigits(personnummer) == 10:
        return personnummer[0:6] + '-' + personnummer[6:]
    else:
        return 'okänd'

def fixNbr(nbr, char):
    str(nbr.replace(" ", ""))
    nbr = ''.join(char for char in nbr if char.isdigit())
    return nbr + char

def modifyRow(row):
    row = row[columns_to_keep].copy()
    row['Distrikt'] = row['Distrikt'].lower().capitalize()
    row['Tjänst'] = taskMapping[row['Tjänst'].lower()]
    row['Tid'] = format_time(str(row['Tid']))
    row['Pers.nr.'] = personnummer(str(row['Pers.nr.']))
    district = placeMapping[row['Distrikt'].lower()].lower()
    op = taskMapping[row['Tjänst'].lower()]
    row['Kostnad'] = str(price_place_task[district][op]).replace(" ", "")
    row['Resor (kostnad)'] = fixNbr(str(row['Resor (kostnad)']), ' kr')
    row['Resor (km)'] = fixNbr(str(row['Resor (km)']), ' km')
    
    if row['Kostnad'] != '?':
        row['Kostnad'] = str(row['Kostnad']) + ' kr'
    addTime(row)
    return row

def addTime(row):
    if row['Tjänst'] == 'Blod':
        count = 0
        

def copyRow_exact(data, i):
    row = data.iloc[i].copy()
    return row

def validPlace(place):
    if place == '':
        return False
    for p in places:
        if place in p.aliases:
            return True
    return False

def valid_row(row):
    if (isinstance(row, int) or isinstance(row, str)) or str(row['Distrikt']).lower() == "":
        return False
    if not validPlace(str(row['Distrikt']).lower()):
        return False
    if not is_valid_time_format(str(row['Tid'])):
        return False
    if str(row['Tjänst']).lower() not in taskMapping:
        return False
    if numberOfDigits(str(row['Pers.nr.'])) != 4 and numberOfDigits(str(row['Pers.nr.'])) != 6 and numberOfDigits(str(row['Pers.nr.'])) != 10 and str(row['Pers.nr.']).replace(" ", "").lower() != 'okänd':
        return False
    if not valid_date(str(row['Datum'])):
        return False
    return True


#8 col
def fillMap(map, df, krim):
    for i in range(df.shape[0]):    #iterate map with regular places
        row = copyRow_exact(df, i)
        misnamed = Place("misnamed", {"misnamed", "felnamn"})
        for place in map:
            site = str(row.loc['Distrikt']).lower()

            if site in place.aliases and not row.empty:
                if place == södertälje:
                    print(df.iloc[i])
                if valid_row(df.iloc[i]):
                    map[place].loc[len(map[place].reset_index(drop=True))] = modifyRow(row)
                else:
                    map[misnamed].loc[len(map[misnamed].reset_index(drop=True))] = row
                break
    """ for i in range(krim.shape[0]):  #iterate map with krimvården
        row = copyRow_exact(krim, i)
        if not row.empty:
            p = Place("krim", ["kvv", "krim"])
            if valid_row(str(row.loc['Tjänst'])):
                map[p].loc[len(map[p])] = modifyRow(row)
            else:
                map[misnamed].loc[len(map[misnamed])] = row """
    return map

""" def createPlaces():  #manually create the places
    norrtalje = Place("norrtälje", {"norrtälje"})
    sodertalje = Place("södertälje", {"södertälje"})
    syd = Place("syd", {"syd", "flemingsberg", "nacka", "flempan", "söderort", "stockholm syd", "västberga"})
    city = Place("city", {"city", "norrmalm", "söder", "kungsholmen", "vasastan", "östermalm", "city", "stockholm city", "stockholm", "söder", "södermalm", "söderort"})
    krim = Place("krim", {"krim", "kvv"})
    misnamed = Place("misnamed", {"misnamed", "felnamn"})
    nord = Place("nord", {"nord", "norrort","norrort", "nord", "solna"})
    return [norrtalje, sodertalje, syd, city, misnamed, krim, nord]
 """
def getDistrictData(name, map):
    for place in map:
        if name in place.aliases:
            return map[place]

def sameColumns(col1, col2):
    for i in range(len(col1)-1):
        if col1[i] != col2[i]:
            return False
    return True

def run(path, map, runProgram):
    data, krim = getDataFrames(path)
    if not sameColumns(data.columns, required_columns):
        return path.split("/")[-1]
    if not runProgram:
        return ""
    fillMap(map, data, krim)
    print(map[södertälje])
    return ""

def iter_folder(folder_path, target_folder):
    map = {}
    filesWithWrongFormat = []
    runProgram = True
    for place in places:
        map[place] = pd.DataFrame(columns=columns_to_keep)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.xls'):
            success = run(file_path, map, runProgram)
            if success != "":
                filesWithWrongFormat.append(success)
                runProgram = False
    #if runProgram:
    for place in places:
        outputPath = target_folder + "/" + str(place)
        write(outputPath, map[place], place)
    return filesWithWrongFormat


#iter_folder("/Users/victorpekkari/Documents/salg/created", "testcreatedC")

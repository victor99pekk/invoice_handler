import os
import xlsxwriter as xlsx
import random
from Constants import *
import string


def create_xls_file(file_path):
    # Create an empty file
    open(file_path, 'w').close()

def createTime():
    threeNbr = random.randint(0, 2)
    length = 5

    char = random.choice([':', '.'])
    string = ""

    if threeNbr == 0:
        length = 4
    for i in range(length):
        if i == 2:
            string = char + string
            continue
        if i == 1:
            nbr = str(random.randint(0, 6))
        elif i == 0:
            nbr = str(random.randint(0, 9))
        elif i == 3:
            nbr = str(random.randint(0, 9))
        else:
            nbr = str(random.randint(0, 2))
        string = nbr + string
    return string


def createDate():
    return '2403' + str(random.randint(1, 30))

def getDistrict():
    choice = random.choice(list(placeMapping.keys()))
    while choice == 'krim' or choice == 'kvv':
        choice = random.choice(list(placeMapping.keys()))
    return choice

def getTask():
    return random.choice(list(taskMapping.keys()))

def persNbr():
    string = ""
    length = 4
    nbr = random.randint(0, 2)
    if nbr == 0:
        return 'okänd'
    elif nbr == 1:
        length = 6
    for i in range(length):
        string += str(random.randint(0,9))
    return string

def random_string():
    length = random.randint(1, 12)
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def cost():
    cost = str(random.randint(1000, 10000))
    randomNbr = random.randint(0, 2)
    if randomNbr == 0:
        return cost
    elif randomNbr == 1:
        return cost + 'kr'
    else:
        return cost + ' kr'

def Moms():
    rand = random.randint(0, 3)
    if rand == 0:
        return str(random.random())[:4]
    if rand == 1:
        return str(random.random())[:4]
    if rand == 2:
        return str(random.randint(0, 50)) + '%'
    if rand == 3:
        return str(random.randint(0, 50)) + ' %'
    
def travels():
    rand = random.randint(0,3)
    if rand == 0:
        return '0'
    elif rand == 1:
        return str(random.randint(1, 80))
    elif rand == 2:
        return str(random.randint(1, 80)) + 'km'
    elif rand == 3:
        return str(random.randint(1, 80)) + ' km'

def boxValue(stringA):
    if stringA == 'Datum':
        return createDate()
    elif stringA == 'Tjänst':
        return getTask()
    elif string == "Moms (resa)":
        res = Moms()
        return res
    elif stringA == 'Resor(km)':
        res = travels()
        return res
    elif stringA == 'Tid':
        return createTime()
    elif stringA == 'Distrikt':
        return getDistrict()
    elif stringA == 'Pers.nr.':
        return persNbr()
    elif stringA == 'Kostnad' or stringA == 'Momsbelopp' or stringA  == 'Resor(kostnad)':
        return cost()
    
def boxValueNbr(nbr):
    if nbr == 0:
        return createDate()
    elif nbr == 1:
        return createTime()
    elif nbr == 2:
        res = getDistrict()
        return res
    elif nbr == 3:
        res = getTask()
        return res
    elif nbr == 4:
        return persNbr()
    elif nbr == 5:
        return random_string()
    elif nbr == 6:
        return cost()
    elif nbr == 7:
        return Moms()
    elif nbr == 9:
        return travels()

    return cost()


def write(fileName):
    file = path_to_salg + '/created/' + fileName + file_format
    os.makedirs(os.path.dirname(file), exist_ok=True)

    if not os.path.exists(file):
        create_xls_file(file)

    # Create a new workbook and sheet
    workbook = xlsx.Workbook(file)
    workbook = xlsx.Workbook(file, {'nan_inf_to_errors': True})
    sheet = workbook.add_worksheet('Sheet2')
    yellow_format = workbook.add_format({'bg_color': 'yellow', 'font_size': 14, 'bold':True})

    column_width = 20  # 20 characters wide
    sheet.set_column(0, len(required_columns) - 1, column_width)
    header_format = workbook.add_format({'font_size': 20})  # Adjust font size as needed
    sheet.write(0, 0, fileName.split("/")[0], header_format)

    # Write column names to the first row
    for j, col_name in enumerate(required_columns):
        sheet.write(input_start_row, j, col_name, yellow_format)

    # Write the DataFrame data
    for i in range(input_start_row+1, 200):
        for j in range(len(required_columns)-1):
            col = required_columns[j]
            sheet.write(i, j, boxValueNbr(j))   
            #sheet.write(i, j, boxValue(str(required_columns[j])).replace(' ', '').lower().capitalize())   

    # Save the workbook to the file
    workbook.close()

def create_10_files():
    for i in range(10):
        file = 'file' + str(i)
        write(file, )
create_10_files()


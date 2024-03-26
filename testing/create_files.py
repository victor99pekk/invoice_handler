import os
import xlsxwriter as xlsx
import random
from Constants import *
import string

letters = ['a', 'b', 'c', 'd', 'e', 'f', ',', '-', '?', '+', '+', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u']
empty_odds = 1
bigOdd = 100
nbr_rows = 100

def create_xls_file(file_path):
    # Create an empty file
    open(file_path, 'w').close()

def createTime():

    emptyReturn()

    threeNbr = random.randint(0, 2)
    length = 5

    char = random.choice([':', '.'])
    #char = ':'
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

def emptyReturn():
    if random.randint(0, bigOdd) < empty_odds:
        return ''    


def createDate():
    return '23' + '03' + str(random.randint(0, 2)) + str(random.randint(0, 9))

def getDistrict(map):
    take = map
    if random.randint(0, bigOdd) < empty_odds:  # 20% chance for an empty string or non-placeMapping string
        if random.randint(0, 1) == 0:  # 50% chance for an empty string
            return ""
        else:
            return random_string()
    choice = random.choice(list(take.keys()))
    while choice == 'krim' or choice == 'kvv':
        choice = random.choice(list(take.keys()))
    if choice == 'södertalje':
        return 'Södertälje' if random.randint(0, 1) == 0 else 'södertälje'  # Randomly capitalize 'södertalje'
    return choice.capitalize() if random.randint(0, 1) == 0 else choice  # Randomly capitalize the returned string

def persNbr():
    # Introduce randomness for "okänd", "xxx", or a random string
    rand_num = random.randint(0, 100)
    if rand_num < 5:  # 5% chance for "okänd"
        return "okänd"
    elif rand_num < 10:  # 5% chance for "xxx"
        length = random.randint(1, 10)  # Vary length between 1 and 10 characters
        return "x" * length
    elif rand_num < empty_odds:  # 10% chance for an empty string
        return ""

    string = ""
    length = random.randint(4, 6)  # Randomize length between 4 and 6
    for i in range(length):
        if random.randint(0, 10) < 2:  # 20% chance to add a non-numeric character
            string += random.choice(letters)  # Add a random letter
        else:
            string += str(random.randint(0, 9))
    return string


def random_string():
    length = random.randint(1, 12)
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def cost():
    rand_num = random.randint(0, bigOdd)
    if rand_num < empty_odds:  # 10% chance for an empty string
        return ""
    elif rand_num < empty_odds:  # 10% chance for a random string
        return random_string()

    cost_value = str(random.randint(1000, 10000))
    randomNbr = random.randint(0, 2)
    if randomNbr == 0:
        return cost_value
    elif randomNbr == 1:
        return cost_value + 'kr'
    else:
        return cost_value + ' kr'


def Moms():
    rand_num = random.randint(0, bigOdd)
    if rand_num < empty_odds:  # 10% chance for an empty string
        return ""
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
    rand_num = random.randint(0, bigOdd)
    if rand_num < empty_odds:  # 10% chance for an empty string
        return ""
    emptyReturn()
    rand = random.randint(0,3)
    if rand == 0:
        return '0'
    elif rand == 1:
        return str(random.randint(1, 80))
    elif rand == 2:
        return str(random.randint(1, 80)) + 'km'
    elif rand == 3:
        return str(random.randint(1, 80)) + ' km'

    
def boxValueNbr(nbr):
    if nbr == 0:
        return createDate()
    elif nbr == 1:
        return createTime()
    elif nbr == 2:
        res = getDistrict(placeMapping)
        return res
    elif nbr == 3:
        res = getDistrict(taskMapping)
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
    for i in range(input_start_row+1, nbr_rows):
        for j in range(len(required_columns)-1):
            if random.randint(0, 100) < empty_odds:
                continue
            string = boxValueNbr(j)
            sheet.write(i, j, string)   
            #sheet.write(i, j, boxValue(str(required_columns[j])).replace(' ', '').lower().capitalize())   

    # Save the workbook to the file
    workbook.close()

def create_10_files():
    for i in range(4):
        file = 'file' + str(i)
        print(file)
        write(file, )
create_10_files()


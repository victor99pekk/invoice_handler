import math
import os
import xlsxwriter as xlsx
from Config import *
import datetime
import pandas as pd
from abc import ABC, abstractmethod
from Row import Row
from Place import Place

class WriteChooser:

    def __init__(self, output_folder: str=None):
        self.output_folder = output_folder
        self.excel_writer = ExcelWriter(output_folder)
        self.error_writer = ErrorWriter(output_folder)
        self.drop_writer = DropWriter(output_folder)

    def write(self, place1: 'Place'):
        if 'misnamed' == place1:
            self.error_writer.write(place1)
        elif 'dropped' == place1:
            self.drop_writer.write(place1)
        else:
            self.excel_writer.write(place1)

class Writer(ABC):

    def __init__(self, output_folder: str=None):
        self.folder_path = output_folder
    
    def sort_on_date(self, place):
        if place != 'misnamed':
            df = place.dataframe
            df.sort_values(by=['Datum', 'Tid'], inplace=True)

    def create_and_return_folder(self, filename):
        desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
        file = desktop + path +  self.folder_path + '/' + filename + file_format
        os.makedirs(os.path.dirname(file), exist_ok=True)
        return file
    
    def format_number(self, number_str):
        number = int(number_str)
        formatted_number = '{:,.0f}'.format(number).replace(",", " ")
        return str(formatted_number)
    
    def get_datetime(self, df, i):
        date = str(df.iloc[i]['Datum'])
        time = str(df.iloc[i]['Tid'])
        
        year = '20' + date[0:2]
        month = date[2:4]
        day = date[4:6]
        hour = time[0:2]
        minute = time[3:5]
        return datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=0)

    
    def half_hour_diff(self, df, timediff, index):
        if (not Row.valid_time(str(df.iloc[index]['Tid']))) or (not Row.valid_time(str(df.iloc[index-1]['Tid']))):
            return False
        dateA = self.get_datetime(df, index)
        dateB = self.get_datetime(df, index - 1)
        difference = abs(dateB - dateA)
        correct_timeDiff = (difference  < datetime.timedelta(minutes=timediff+1))
        correct_task = str(df.iloc[index-1]['Tjänst']) == 'Blod' and str(df.iloc[index]['Tjänst']) == 'Blod'
        correct_district = str(df.iloc[index-1]['Distrikt']) == str(df.iloc[index]['Distrikt'])

        return correct_timeDiff and correct_task and correct_district
    
    def write_nan(self, worksheet, row_idx, col_idx, value, format=None):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            value = ''
        worksheet.write(row_idx, col_idx, value, format)
    
    @abstractmethod
    def write(self):
        pass


class DropWriter(Writer):
    def __init__(self, output_folder: str=None):
        super().__init__(output_folder)

    def write(self, place):

        file_name = self.create_and_return_folder(place.name)
        df = place.dataframe

        workbook = xlsx.Workbook(file_name, {'nan_inf_to_errors': True})
        sheet = workbook.add_worksheet('Sheet2')
        yellow = workbook.add_format({'bg_color': 'yellow', 'font_size': 14, 'bold':True, 'border': 1})

        column_width = 20  # 20 characters wide
        sheet.set_column(0, len(place.dataframe.columns) - 1, column_width)
        header = workbook.add_format(header_format)  # Adjust font size as needed
        small_text = workbook.add_format(small_text_format)
        error = workbook.add_format(error_format)

        # sheet.write(0, 0, str(place.name.capitalize()), header)
        # sheet.write(0, 1, 'skapades: ' + str(datetime.date.today()), small_text)
        self.write_nan(sheet, 0, 0, str(place.name.capitalize()), header)
        self.write_nan(sheet, 0, 1, 'skapades: ' + str(datetime.date.today()), small_text)

        # Write column names to the first row
        for j, col_name in enumerate(df.columns):
            # sheet.write(startWrite-1, j, col_name, yellow)
            self.write_nan(sheet, startWrite-1, j, col_name, yellow)

        # Write the DataFrame data
        for i, row in enumerate(df.values):
            row_ = Row(df.iloc[i])
            for j, value in enumerate(row_.data):
                if j == 0:
                    value = str(df['Datum'].iloc[i])
                # else:
                # sheet.write(startWrite + i, j, value)  # Start writing data from the third row
                self.write_nan(sheet, startWrite + i, j, value)
                
                if df.columns[j] == 'Tid' and not pd.isna(df.columns[j]):
                    # sheet.write(startWrite + i, j, value)
                    self.write_nan(sheet, startWrite + i, j, value)
                elif df.columns[j] == 'Tid':
                    # sheet.write(startWrite + i, j, "  --  ")
                    self.write_nan(sheet, startWrite + i, j, "  --  ", error)

        # Save the workbook to the file
        workbook.close()
    

class ErrorWriter(Writer):
    def __init__(self,output_folder: str=None):
        super().__init__(output_folder)

    def write(self, place):

        file_name = self.create_and_return_folder(place.name)
        df = place.dataframe

        workbook = xlsx.Workbook(file_name, {'nan_inf_to_errors': True})
        sheet = workbook.add_worksheet('Sheet2')
        yellow = workbook.add_format({'bg_color': 'yellow', 'font_size': 14, 'bold':True, 'border': 1})

        column_width = 20  # 20 characters wide
        sheet.set_column(0, len(place.dataframe.columns) - 1, column_width)
        header = workbook.add_format(header_format)  # Adjust font size as needed
        small_text = workbook.add_format(small_text_format)
        error = workbook.add_format(error_format)

        # sheet.write(0, 0, str(place.name.capitalize()), header)
        # sheet.write(0, 1, 'skapades: ' + str(datetime.date.today()), small_text)
        self.write_nan(sheet, 0, 0, str(place.name.capitalize()), header)
        self.write_nan(sheet, 0, 1, 'skapades: ' + str(datetime.date.today()), small_text)

        # Write column names to the first row
        for j, col_name in enumerate(df.columns):
            #if j == 0 or j == len(df.columns) - 1:  # First and last columns    
            # sheet.write(startWrite-1, j, col_name, yellow)
            self.write_nan(sheet, startWrite-1, j, col_name, yellow)
        
        # Write the DataFrame data
        for i, row in enumerate(df.values):
            row_ = Row(df.iloc[i])
            for j, value in enumerate(row):
                if j == 0:
                    value = str(df['Datum'].iloc[i])
                if str(df.columns[j]) in row_.bool_mapping and (not row_.bool_mapping[str(df.columns[j])]):
                    # sheet.write(startWrite + i, j, value, error)
                    self.write_nan(sheet, startWrite + i, j, value, error)
                else:
                    # sheet.write(startWrite + i, j, value)  # Start writing data from the third row
                    self.write_nan(sheet, startWrite + i, j, value)
                
                if df.columns[j] == 'Tid' and not pd.isna(df.columns[j]):
                    # sheet.write(startWrite + i, j, value)
                    self.write_nan(sheet, startWrite + i, j, value)
                elif df.columns[j] == 'Tid':
                    # sheet.write(startWrite + i, j, "  --  ", error)
                    self.write_nan(sheet, startWrite + i, j, "  --  ", error)

        # Save the workbook to the file
        workbook.close()
        

class ExcelWriter(Writer):

    def __init__(self, folder_path: str=None):
        super().__init__(folder_path)
    
    def write(self, place: 'Place'):
        self.sort_on_date(place)

        workbook = xlsx.Workbook(self.create_and_return_folder(place.name), {'nan_inf_to_errors': True})
        sheet = workbook.add_worksheet('Sheet2')
        yellow = workbook.add_format(yellow_format)

        column_width = 20  # 20 characters wide
        sheet.set_column(0, len(place.dataframe.columns) - 1, column_width)
        header = workbook.add_format(header_format)  # Adjust font size as needed
        small_text = workbook.add_format(small_text_format)
        light_blue = workbook.add_format(light_blue_format)
        header_light_blue = workbook.add_format(header_light_blue_format)

        # write name of the district to the top right corner of excel file
        self.write_nan(sheet, 0, 0, str(place.name.capitalize()), header)
        self.write_nan(sheet, 0, 1, 'skapades: ' + str(datetime.date.today()), small_text)


        # start writing the rows to the excel file
        
        # Write column names to the first row
        for j, col_name in enumerate(place.dataframe.columns):
            self.write_nan(sheet, startWrite-1, j, col_name, yellow)


        # Write occurrences of the different tasks
        sheet.write(startWrite-3, 0, 'Antal', header_light_blue)
        sheet.write(startWrite-2, 0, 'Totalt Pris', header_light_blue)

        discount_count = 0
        map = place.job_occurence

        for index in range(1, len(place.dataframe)):
            if self.half_hour_diff(place.dataframe, 30, index):
                #place.dataframe.loc[index, 'Kostnad'] = '(rabatt)                  ' + rabatt
                place.dataframe.at[index, 'Kostnad'] = '(rabatt)                  ' + rabatt
                discount_count += 1
        for j, task in enumerate(set(taskMapping.values())):
            price = place.get_price(str(task)) # this function will return none if the task is not in the dictionary
            if price == 0 or (task.lower() == 'läkemedel' or task.lower() == 'medicin'):
                #price = int(place.dataframe.iloc[j]['Kostnad'])
                price = " -- "
            if str.isdigit(str(price)):
                if task == 'Blod':
                    self.write_nan(sheet, startWrite-4, 1 + j, (task +'(Pris='+str(price)+'kr)'), header_light_blue)
                    self.write_nan(sheet, startWrite-3, 1 + j, str(map.get(task, 0)-discount_count)+',   rabatt: '+str(discount_count), light_blue)
                    self.write_nan(sheet, startWrite-2, 1 + j, self.format_number( str((int(price) * (int(map.get(task, 0))-discount_count)) + (discount_count* int(rabatt)))) , light_blue)
                else:
                    self.write_nan(sheet, startWrite-4, 1 + j, (task +'(Pris='+str(price)+'kr)'), header_light_blue)
                    self.write_nan(sheet, startWrite-3, 1 + j, map.get(task, 0), light_blue)
                    self.write_nan(sheet, startWrite-2, 1 + j, self.format_number( str((int(price) * (int(map.get(task, 0)))) )), light_blue)
            
            else:
                self.write_nan(sheet, startWrite-4, 1 + j, (task +'(Pris= ?)'), header_light_blue)
                self.write_nan(sheet, startWrite-3, 1 + j, map.get(task, 0), light_blue)
                if (task.lower() == 'läkemedel' or task.lower() == 'medicin'):
                    self.write_nan(sheet, startWrite-2, 1 + j, "räkna för hand ", light_blue)
                else:
                    self.write_nan(sheet, startWrite-2, 1 + j, "tjänst finns ej i distriktet", light_blue)

        
        # Write the dataframe to the excel file
        for i, row in enumerate(place.dataframe.values):
            for j, value in enumerate(row):
                if j == 0:
                    # value = self.convert_date(str(self.df['Datum'].iloc[i]))
                    date = str(place.dataframe['Datum'].iloc[i])
                    value = date[4:6] + '/' + date[2:4] + '-' + '20' + date[0:2]
                    # sheet.write(startWrite + i, j, value)
                    self.write_nan(sheet, startWrite + i, j, value)
                else:
                    # sheet.write(startWrite + i, j, value)  # Start writing data from the third row
                    self.write_nan(sheet, startWrite + i, j, value)
        # Save the workbook to the file
        workbook.close()



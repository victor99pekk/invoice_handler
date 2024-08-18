from Config import *
import pandas as pd

class Row:
    def __init__(self, data: pd.Series):
        self.data = data.copy()
        self.addrow()
        self.bool_mapping = self.get_validity_mapping()
        self.update_values()

    def get_validity_mapping(self):
        return {
            'Datum': self.valid_date(),
            'Distrikt': self.valid_place_slow(),
            'Tjänst': self.valid_task_slow(),
            'Tid': Row.valid_time(self.time_str)
        }
    
    def update_values(self):
        if self.bool_mapping['Datum']:
            self.date_str = str(self.date_str)
            if len(self.date_str) == 8:
                self.date_str = self.date_str[2:]
        if self.bool_mapping['Distrikt']:
            self.district = self.district.lower().capitalize().strip()
        if self.bool_mapping['Tjänst']:
            self.task = taskMapping[self.task.lower()].capitalize()
        if self.bool_mapping['Tid']:
            self.time_str = self.format_time(str(self.time_str))

        # self.data['Datum'] = self.date_str
        # self.data['Distrikt'] = self.district
        # self.data['Tjänst'] = self.task
        # self.data['Tid'] = self.time_str
        self.data.loc['Datum'] = self.date_str
        self.data.loc['Distrikt'] = self.district
        self.data.loc['Tjänst'] = self.task
        self.data.loc['Tid'] = self.time_str
    
    def valid_row(self):
        for key in self.bool_mapping:
            if not self.bool_mapping[key] and key != 'Tid':
                return False
        return True
    
    def format_time(self, time_str):
        if len(time_str) == 4 and self.numberOfDigits(time_str) == 4:
            return time_str[0:2] + ':' + time_str[2:]
        elif len(time_str) == 4:
            return '0' + time_str[0] + ':' + time_str[2:]
        elif len(time_str) == 5: 
            return time_str[:2] + ':' + time_str[3:]
        
        if self.numberOfDigits(time_str) != 4:
            return str(time_str)[:5]

    def addrow(self):
        data = self.data
        self.date_str = data['Datum']
        self.time_str = data['Tid']
        self.district = data['Distrikt']
        self.task = data['Tjänst']
        self.pers_nr = data['Pers.nr.']
        self.k_nummer = data['K-nummer']
        self.moms = data['Moms']
        self.resor_km = data['Resor (km)']
        self.resor_kostnad = data['Resor (kostnad)']
        self.kostnad = data['Kostnad']
        self.lakare = data['Läkare']
    
    def get_element(self, key: str):
        return self.data.loc[key]
    @staticmethod
    def numberOfDigits(string):
        string = str(string)
        return sum(c.isdigit() for c in string)
    
    def valid_date(self):
        date_str = str(self.date_str)
        if (Row.numberOfDigits(date_str) != 8) and (Row.numberOfDigits(date_str) != 6) or len(date_str) != Row.numberOfDigits(date_str):
            return False

        if len(date_str) == 8 and str(date_str)[0] == '2' and str(date_str)[1] == '0':
            date_str = str(date_str)[2:]
        if len(str(date_str)) == 1 and self.numberOfDigits(str(date_str)) == 1 and float(date_str) < 1 and float(date_str) > 0:
            return True
        if (self.numberOfDigits(date_str) != 6):
            return False
        if date_str.lower() == '':
            return False
        if date_str[5] == '0' and date_str[4] == '0':
            return False
        if date_str[2] == '0' and str(date_str)[3] == '0':
            return False
        return True
    
    def valid_place(self):
        place = self.district.lower().strip()
        if place == '' or place not in existing_places:
            return False
        return True
    
    def valid_place_slow(self):
        if not isinstance(self.district, str):
            return False
        place = self.district.lower().strip()
        for existing_place in existing_places:
            if place in existing_place.lower() or existing_place.lower() in place:
                return True
        return False
    
    @staticmethod
    def valid_time(time):
        time = str(time)
        char = ['.', ':']
        if Row.numberOfDigits(time) == 6 and ':' in str(time) and time[6] == '0' and time[7] == '0' and time[5] == time[2]:
            return True
        if len(time) == 4 and Row.numberOfDigits(time) == 4:
            if int(time[0]) == 2 and int(time[1]) < 4 and int(time[2]) < 6:
                return True
            elif int(time[0]) < 2 and int(time[1]) <= 9 and int(time[2]) < 6:
                return True        
        elif Row.numberOfDigits(time) == 4 and len(time) == 5 and str(time[2]) in char:
            if int(time[0]) == 2 and int(time[1]) < 4 and int(time[3]) < 6:
                return True
            elif int(time[0]) < 2 and int(time[1]) <= 9 and int(time[3]) < 6:
                return True
        elif Row.numberOfDigits(time) == 3 and len(time) == 4 and str(time[1]) in char:
            if int(time[0]) <= 9 and int(time[2]) < 6 and int(time[3]) <= 9:
                return True
        return False
    
    def valid_task(self):
        task = self.task
        if task == '' or task.lower() not in taskMapping:
            return False
        return True
    
    def valid_task_slow(self):
        if not isinstance(self.task, str):
            return False
        task = self.task.lower()
        for existing_task in taskMapping:
            if task in existing_task or existing_task in task:
                self.task = existing_task
                self.data.loc['Tjänst'] = existing_task
                return True
        return False
    

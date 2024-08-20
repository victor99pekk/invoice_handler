from collections.abc import Iterable
import pandas as pd
from Config import *


class Place:
    def __init__(self, name, synonyms: Iterable, dataframe: pd.DataFrame=None, error: bool=False, task_prices: dict=None):
        self.name = name
        self.synonyms = set(synonyms)
        if 'dropped' == name:
            cols = dropped_columns
        else:
            cols = columns_to_keep
        self.dataframe = pd.DataFrame(columns=cols)
        self.job_occurence = {}
        self.task_prices = task_prices

    def __str__(self):
        return f'{self.name}\n\n{self.dataframe}'
    
    def contains(self, place: str):
        for syn in self.synonyms:
            if syn in place.lower().strip() or place.lower().strip() in syn:
                return True
        # return place.lower().strip() in self.synonyms   # only checking exakt match
    
    def add_data(self, data: pd.Series):    # series to be added must be good format
        if self.name != 'misnamed':
            task = taskMapping[str(data['Tjänst']).lower()]
            self.job_occurence[task] = self.job_occurence.get(task, 0) + 1
        # self.dataframe = self.dataframe.append(data, ignore_index=True)
        self.dataframe.loc[len(self.dataframe.reset_index(drop=True))] = data
    # map[place].loc[len(map[place].reset_index(drop=True))] = modifyRow(row, site_connection)
    def get_price(self, task: str):
        task = task.lower().strip()
        return self.task_prices.get(task.capitalize(), 0)
    
    def concat_dataframe(self, other: pd.DataFrame):
        self.dataframe = pd.concat([self.dataframe, other], ignore_index=True)
    
    def __eq__(self, value: str) -> bool:
        return self.name == value






import pandas as pd

from Row import Row
class File:
    def __init__(self, path: str=None):
        self.path = path
        self.droped_values = pd.DataFrame()
        self.dataframe, self.droped_values = self.get_dataframe()
        self.start = 0

    def start_row(self, df, list_of_names):
        for names in list_of_names:
            list = df.index[df.iloc[:, 0] == names].tolist()
            if len(list) > 0:
                return list[0] + 1
        return -1
    
    def get_dataframe(self):
        df = pd.read_excel(self.path)

        self.start = self.start_row(df, ["Datum"])    # Find the row where the data starts
        # Create a new DataFrame without the first n rows
        data = df.iloc[self.start:].copy()
        data.rename(columns=df.iloc[self.start-1], inplace=True)
        data.dropna(how='all', inplace=True)

        dropped_rows = data[data[['Distrikt', 'Tjänst']].isna().any(axis=1)].copy()
        dropped_rows['RowNumber'] = data[data[['Distrikt', 'Tjänst']].isna().any(axis=1)].index + 2
        dropped_rows['filename'] = self.path.split("/")[-1]


        data.dropna(subset=['Distrikt', 'Tjänst'], inplace=True)
        
        data['Läkare'] = df.iloc[0,1]
        return data, dropped_rows
    
    def sort(self, place_list):
        dataframe = self.dataframe
        place_list[-1].concat_dataframe(self.droped_values)
        for i in range(len(dataframe)):    #iterate map with regular places
            row = Row(dataframe.iloc[i].copy())
            added = False
            if not row.valid_row():
                place_list[0].add_data(row.data)
                continue
            
            for place in place_list:
                if place.contains(row.get_element('Distrikt')):
                    place.add_data(row.data)
                    added = True
                    break
            if not added:
                droped_row = row.data.copy() 
                droped_row['RowNumber'] = self.start + i
                droped_row['filename'] = self.path.split("/")[-1]
                place_list[-1].add_data(droped_row)

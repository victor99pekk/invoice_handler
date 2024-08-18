import os
from ExcelWriter import WriteChooser
from File import File
from Place import Place
from Config import *

class Environment:

    def __init__(self):
        self.misnamed = Place('misnamed', synonyms=["misnamed"])
        self.nord = Place('nord', synonyms=["solna","västerort", "arlanda", "nord", "norrort","norrort", "nord", "solna", "norrort"], 
                          task_prices={'Blod': 1800, 'Arrestvård': 2300, 'Död': 7000, 'Rape kit': 7200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':2000})
        self.syd = Place('syd', synonyms=["södertörn", "syd", "flemingsberg", "nacka", "flempan", "söderort", "stockholm syd", "västberga"],
                         task_prices={'Blod': 2200, 'Arrestvård': 2200, 'Död': 7000, 'Rape kit': 5000, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':2000})
        self.norrtalje = Place('norrtälje', synonyms=["norrtälje", "norrtalje"],
                               task_prices={'Jourläkare': 2000, 'Blod': 3000, 'Arrestvård': 3120, 'Död': 3240, 'Rape kit': 7200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':2000})
        self.sodertalje = Place('södertälje', synonyms=["södertälje", "södertalje", "sodertalje", "sodertälje"],
                                task_prices={'Jourläkare': 2000, 'Blod': 3000, 'Arrestvård': 3120, 'Död': 3240, 'Rape kit': 7200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':2000})
        self.city = Place('city', synonyms=["kronoberg", "city", "norrmalm", "kungsholmen", "vasastan", "östermalm", "city", "stockholm city", "stockholm", "södermalm", "söderort"],
                          task_prices={'Blod': 3900, 'Arrestvård': 900, 'Död': 7000, 'Rape kit': 5200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':2000})
        self.dropped = Place('dropped', synonyms=["dropped"])
        self.place_list = [self.misnamed, self.nord, self.syd, self.norrtalje, self.sodertalje, self.city, self.dropped]

    def iterate_input(self, folder_path, target_folder):
        filesWithWrongFormat = []

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and (filename.endswith('.xls') or filename.endswith('.xlsx')):
                success = self.run(file_path, self.place_list)
                if success != "":
                    filesWithWrongFormat.append(success)
                    #runProgram = False
        writer = WriteChooser(target_folder)
        #if runProgram:
        
        for place in self.place_list:
            writer.write(place1=place)
        return filesWithWrongFormat
    
    def sameColumns(self, col1):
        copiedArray = [s.strip().lower() if isinstance(s, str) else s for s in col1]
        for column in must_have_columns:
            if column.lower() not in copiedArray:
                return False
        return True
    
    def run(self, file_path, place_list):
        file = File(file_path)

        if not self.sameColumns(file.dataframe.columns):
            return path.split("/")[-1]
        # if not runProgram:
        #     return ""
        file.sort(place_list)
        return ""
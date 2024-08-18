# Description: Configuration file for the program

#lägg till här och i enviroment då place skapad
existing_places = {"västerort", "arlanda", "solna", "norrort","södertörn","tälje", "syd", "flemingsberg", "nacka", "flempan", "söderort", "stockholm syd", "västberga", "city", "norrmalm", "kungsholmen", "vasastan", "östermalm", "city", "stockholm city", "stockholm", "södermalm", "söderort"}

# -------------------

columns_to_keep = ['Datum','Tid', 'Distrikt', 'Tjänst', 'Pers.nr.','K-nummer', 'Moms', 'Resor (km)', 'Resor (kostnad)', 'Kostnad', 'Läkare']

# -------------------

must_have_columns = ['Datum','Tid','Distrikt','Tjänst','Pers.nr.','K-nummer']

# -------------------

path = '/salg_fakturor/'

# -------------------

file_format = '.xlsx'

# -------------------

input_start_row = 9

# -------------------

startWrite = 10

# -------------------

rabatt = '1200'

# -------------------

taskMapping = {}
taskMapping['medicin'] = 'Läkemedel'
taskMapping['läkemedel'] = 'Läkemedel'
taskMapping['blodprov'] = 'Blod'
taskMapping['blod'] = 'Blod'
taskMapping['medicinsk undersökning'] = 'Arrestvård'
taskMapping['arrestvård'] = 'Arrestvård'
taskMapping['död'] = 'Död'
taskMapping['dödsfall'] = 'Död'
taskMapping['rape-kit'] = 'Rape kit'
taskMapping['rape kit'] = 'Rape kit'
taskMapping['Rape kit'] = 'Rape kit'
taskMapping['rättintyg'] = 'kroppsbesiktning+rättsintyg'
taskMapping['rättsintyg'] = 'kroppsbesiktning+rättsintyg'
taskMapping['kroppsbesiktning+rättsintyg'] = 'kroppsbesiktning+rättsintyg'
taskMapping['kroppsbesiktning'] = 'kroppsbesiktning+rättsintyg'
taskMapping['blodprov1'] = 'Blod'
taskMapping['blodprov2'] = 'Blod'
taskMapping['Jourläkare'] = 'Jourläkare'
taskMapping['jourläkare'] = 'Jourläkare'


# -------------------
# excel writer format

yellow_format = {'bg_color': 'yellow', 'font_size': 14, 'bold':True, 'border': 1}
column_width = 20  # 20 characters wide
header_format = {'font_size': 20}  # Adjust font size as needed
small_text_format = {'font_size': 10}
light_blue_format = {'bg_color': '#ADD8E6', 'border': 1}
header_light_blue_format = {'bg_color': '#ADD8E6', 'border': 1, 'bold':True}
error_format = {'bg_color': 'red', 'font_size': 14, 'bold':True, 'border': 1}

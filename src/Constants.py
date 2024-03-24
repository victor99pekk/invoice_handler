from Place import Place

norrtälje = Place("norrtälje", {"norrtälje"})
södertälje = Place("södertälje", {"södertälje", "södertalje", "sodertalje", "sodertälje"})
syd = Place("syd", {"syd", "flemingsberg", "nacka", "flempan", "söderort", "stockholm syd", "västberga"})
city = Place("city", {"city", "norrmalm", "söder", "kungsholmen", "vasastan", "östermalm", "city", "stockholm city", "stockholm", "söder", "södermalm", "söderort"})
krim = Place("krim", {"krim", "kvv"})
misnamed = Place("misnamed", {"misnamed", "felnamn"})
nord = Place("nord", {"nord", "norrort","norrort", "nord", "solna", "norrort"})
places = [norrtälje, södertälje, syd, city, misnamed, krim, nord]

# -------------------


columns_to_keep = ['Datum','Tid', 'Distrikt', 'Tjänst', 'Pers.nr.', 'Resor (km)', 'Resor (kostnad)', 'Kostnad']

# -------------------

required_columns = ['Datum','Tid','Distrikt','Tjänst','Pers.nr.','K-nummer',
                    'Kostnad','Moms','Momsbelopp','Resor (km)','Resor (kostnad)',
                    'Moms (resa)', 'None']

# -------------------

path = '/salg_fakturor/'

# -------------------

discount_blod = {
    'city': set(),
    'nord': set(),
    'syd': set(),
    'södertälje': set(),
    'norrtälje': set(),
    'krim': set(),
    'misnamed': set()
}

# -------------------

file_format = '.xls'

# -------------------

path_to_salg = '/Users/victorpekkari/Documents/salg'

# -------------------

input_start_row = 9

# -------------------

startWrite = 10

# -------------------

taskMapping = {}
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
taskMapping['kroppsbesiktning+rättsintyg'] = 'kroppsbesiktning+rättsintyg'
taskMapping['kroppsbesiktning'] = 'kroppsbesiktning+rättsintyg'
taskMapping['blodprov1'] = 'Blod'
taskMapping['blodprov2'] = 'Blod'

# -------------------

# Example using manual declaration
price_place_task = {
    'krim': {'Blod': '?', 'Arrestvård': '?', 'Död': '?', 'Rape kit': '?', 'Urinprov':'?', 'Utryckning utan uppdrag':'?', 'kroppsbesiktning+rättsintyg':'?'},
    'misnamed': {'Blod': '?', 'Arrestvård': '?', 'Död': '?', 'Rape kit': '?', 'Urinprov':'?', 'Utryckning utan uppdrag':'?', 'kroppsbesiktning+rättsintyg':'?'},
    'city': {'Blod': 3900, 'Arrestvård': 900, 'Död': 7000, 'Rape kit': 5200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':'?'},
    'nord': {'Blod': 1800, 'Arrestvård': 2300, 'Död': 7000, 'Rape kit': 7200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':'?'},
    'syd': {'Blod': 2200, 'Arrestvård': 2200, 'Död': 7000, 'Rape kit': 5000, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':'?'},
    'södertälje': {'Blod': 3000, 'Arrestvård': 3120, 'Död': 3240, 'Rape kit': 7200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':'?'},
    'norrtälje':{'Blod': 3000, 'Arrestvård': 3120, 'Död': 3240, 'Rape kit': 7200, 'Urinprov':1200, 'Utryckning utan uppdrag':1200, 'kroppsbesiktning+rättsintyg':'?'},
}

rabatt = '1200 kr (rabatt)'

placeMapping = {
    'norrort': 'nord',
    'sodertalje': 'södertälje',
    'södertalje': 'södertälje',
    'sodertälje': 'södertälje',
    'solna': 'nord',
    'city': 'city',
    'nord': 'nord',
    'syd': 'syd',
    'södertälje': 'södertälje',
    'krim': 'krim',
    'sollentuna': 'nord',
    'västberga': 'syd',
    'flemingsberg': 'syd',
    'nacka': 'syd',
    'norrmalm': 'city',
    'södermalm': 'city',
    'östermalm': 'city',
    'norrtälje': 'norrtälje',
}

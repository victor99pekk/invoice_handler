# Description: This file contains the Task class and the create_validTasks function

class Task:
    def __init__(self, task, group, place):
        self.group = group
        self.task = task
        self.ValidTasks = create_validTasks()

    @staticmethod
    def create_validTasks():
        tasks = {}
        tasks['blodprov'] = 'Blod'
        tasks['blod'] = 'Blod'
        tasks['medicinsk undersökning'] = 'Arrestvård'
        tasks['arrestvård'] = 'Arrestvård'
        tasks['död'] = 'Död'
        tasks['dödsfall'] = 'Död'
        tasks['rape-kit'] = 'Rape kit'
        tasks['rape kit'] = 'Rape kit'
        tasks['Rape kit'] = 'Rape kit'
        tasks['rättintyg'] = 'kroppsbesiktning+rättsintyg'
        tasks['kroppsbesiktning+rättsintyg'] = 'kroppsbesiktning+rättsintyg'
        tasks['kroppsbesiktning'] = 'kroppsbesiktning+rättsintyg'
        return tasks
    
    @staticmethod
    def price(task, place):
        return 3000

    def __str__(self):
        return self.task
    
    def lower(self):
        return self.task.lower()
    
    def __repr__(self):
        return self.task
    
    def __eq__(self, other):
        return other.lower() in self.group
    
    def __hash__(self):
        return hash(self.name)
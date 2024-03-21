
class Place:

    def __init__(self, name, aliases):
        self.aliases = aliases
        self.name = name
    
    def __str__(self):
        return self.name
    
    def lower(self):
        return self.name.lower()
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        return other.lower() in self.aliases
    
    def __hash__(self):
        return hash(self.name)

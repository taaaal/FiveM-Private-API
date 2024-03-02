import re

class User:
    
    """
    Represents FiveM User
    """
    
    def __init__(self, data):
        self.id   = data.get('id')
        self.name = data.get('name')
        self.ping = data.get('ping')
    
        base_identifiers = ('steam', 'license', 'discord', 'fivem') 
        data_identifiers = data.get('identifiers')
        
        sorted_identifiers = self.sort_identifiers(base_identifiers, data_identifiers)
                              
        self.steam_id   = sorted_identifiers.get('steam_id')
        self.license_id = sorted_identifiers.get('license_id')
        self.discord_id = sorted_identifiers.get('discord_id')
        self.fivem_id   = sorted_identifiers.get('fivem_id')
    
    def sort_identifiers(self, based_identifiers, data_identifiers):
        sorted_identifiers = dict()
        for base_id in base_identifiers:
            for identifier in data_identifiers:
                if identifier.startswith(base_id):
                    proper_identifier = base_id + '_id'
                    clean_identifier_value = self.get_clean_id(identifier)
                    sorted_identifiers[proper_identifier] = clean_identifier_value
        return sorted_identifiers   
                       
    def get_clean_id(self, identifier):
        match = re.match('([a-z]+)\:([a-z0-9]+)', identifier)
        if not match:
            return None
        return match.groups(2)

import re

class User:
    
    def __init__(self, data: dict):
        '''
        User represents by FiveM player
        `data` -> dict | User's data as a dict
        '''
        self.id = data.get('id')
        self.name = data.get('name')
        self.ping = data.get('ping')
    
        based_identifiers = ('steam', 'licenese', 'discord', 'fivem') 
        self.sort_identifiers(based_identifiers, data['identifiers'])
                              
        self.steam_id = self.sorted_identifiers.get('steam_id')
        self.license_id = self.sorted_identifiers.get('license_id')
        self.discord_id = self.sorted_identifiers.get('discord_id')
        self.fivem_id = self.sorted_identifiers.get('fivem_id')
    
    def sort_identifiers(self, based_identifiers, data_identifiers):
        self.sorted_identifiers = dict()
        for k in based_identifiers:
            for v in data_identifiers:
                if v.startswith(k):
                    clean_v = self.get_clean_id(v)
                    clean_k = k + '_id'
                    self.sorted_identifiers[clean_k] = clean_v
                    continue    
                       
    def get_clean_id(self, identifier: str):
        match = re.match('([a-z]+)\:([a-z0-9]+)', identifier)
        if not match:
            return None
        return match.groups()[1]

import asyncio
import json
import aiohttp
import re

'''
Custom Exceptions
'''

class BadIPFormat(Exception):
    pass

class ServerNotRespond(Exception):
    pass

'''
User represented FiveM player
    `data` -> dict | User's data as a dict
'''

class User:
    
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.ping = data.get('ping')
    
        identifiers = ('steam', 'licenese', 'discord', 'fivem') #'live', #'xbl', 'ip')
        sorted_identifiers = dict()
        for k in identifiers:
            for v in data['identifiers']:
                if v.startswith(k):
                    clean_v = self.get_clean_id(v)
                    clean_k = k + '_id'
                    sorted_identifiers[clean_k] = clean_v
                    continue
            
        self.steam_id = sorted_identifiers.get('steam_id')
        self.license_id = sorted_identifiers.get('license_id')
        self.discord_id = sorted_identifiers.get('discord_id')
        self.fivem_id = sorted_identifiers.get('fivem_id')
                       
    def get_clean_id(self, identifier):
        match = re.match('([a-z]+)\:([a-z0-9]+)', identifier)
        if not match:
            return None
        return match.groups()[1]

'''
Server represented FiveM Server Wrapper
    `srvip` -> str       |   Server's IP
    `max_slots` -> int   |   Server's max players
'''
                                          
class Server:
         
    def __init__(self, srvip, max_slots = 32):
        self.srvip = srvip if self.check_ip_format(srvip) is True else None
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_players_data(loop))
        
        self.max_slots = max_slots 
        self.status = False

    def __str__(self):
        return 'FiveM Server'

    def __repr__(self):
        return '<{0.__str__} server_ip={0.srvip} status={0.status}'.format(self)

    def check_ip_format(self, srvip):
        part, port = r'([0-9][0-9][0-9])', r'([0-9][0-9][0-9][0-9][0-9]?)'
        match = re.match('{0}.{0}.{0}.{0}:{1}'.format(part, port), srvip)
        if not match:
            raise BadIPFormat('[ERROR] Incorrect IP format.')
        return True

    async def get_players_data(self, loop):
        async def fetch(session):
            async with session.get('http://{}/players.json'.format(self.srvip)) as resp:
                if resp.status != 200:
                    raise ServerNotRespond('[ERROR] Server is not responding or not found.')
                self.status = True 
                return await resp.read() 

        async with aiohttp.ClientSession(loop=loop) as session:
            data = await fetch(session)    
            self._data = json.loads(data)         

    def _players(self):
        for player in self._data:
            yield User(player)

    @property
    def online_players(self):
        return (len(set(self._players())), self.max_slots)

   #@property
   #def scripts(self):
   #       return self.serverinfo.get("resources", "This server has no scripts.")

   #@property   
   #def developers(self):
   #       return self.serverinfo_vars.get("Developer", "No developers were specified for this server.") 

   #@property
   #def discord(self):
   #       return self.serverinfo_vars.get("Discord", "No discord server was specified for this server.") 

   #@property
   #def pubfeed(self):
   #       return self.serverinfo_vars.get("activitypubFeed", "No activity pub feed was specified for this server.")

   #@property
   #def banner_connecting(self):
   #       return self.serverinfo_vars.get("banner_connecting", "This server has no banner for server connecting.")

   #@property
   #def banner_detail(self):
   #       return self.serverinfo_vars.get("banner_detail", "This server has no detail banner.")

   #@property
   #def license_key_token(self):
   #       return self.serverinfo_vars.get("sv_licenseKeyToken", "No license key token were specified for this server.")

   #@property
   #def max_players(self):
   #       return self.serverinfo_vars.get("sv_maxClients", "No information about max players were specified for this server.")

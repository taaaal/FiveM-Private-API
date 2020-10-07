import asyncio
import json
import aiohttp
import datetime
import re

class BadIPFormat(Exception):
    pass
    
class ServerNotRespond(Exception):
    pass

class User:
    
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.ping = data.get('ping')
        
        self.steam_id = self.get_clean_id(data['identifiers'].get('steam', 'none'))
        self.license_id = self.get_clean_id(data['identifiers'].get('license', 'none')
        self.skype_id = self.get_clean_id(data['identifiers'].get('license', 'none')
        self.discord_id = self.get_clean_id(data['identifiers'].get('live', 'none'))
        self.fivem_id = self.get_clean_id(data['identifiers'].get('fivem', 'none'))
        self.xboxlive_id = self.get_clean_id(data['identifiers'].get('xbl', 'none'))
        self.ipaddress = self.get_clean_id(data['identifiers'].get('ip', 'none'))
                       
   def get_clean_id(self, identifier: str):
        match = re.match('([a-z]+)\:([a-z0-9]+)', identifier)
        if not match:
            return None
        return match.groups()[1]
        
class Server:
    
    def __init__(self, srvip: str, max_slots = 32):
        self.srvip = srvip if self.check_ip_format(srvip) is True
        asyncio.get_event_loop().run_until_complete(self.get_players_data())
        
        self.max_slots = max_slots 
        self.status = False
        
   def __str__(self):
        pass
               
   def __repr__(self):
        pass       
          
    def check_ip_format(self, srvip):
        part, port = r'([0-9][0-9][0-9])', r'([0-9][0-9][0-9][0-9][0-9])'
        match = re.match({0}.{0}.{0}.{0}:{1}.format(part, port), srvip)
        if not match:
            raise BadIPFormat('[ERROR] Incorrect IP format.')
        return True
                     
    async def get_players_data(self)
        async with aiohttp.ClientSession().get('http://{}/players.json'.format(self.srvip)) as resp:
            if resp.status != 200:
               raise ServerNotRespond('[ERROR] Server is not responding or not found.')
                         
            data = await resp.read()         
            self._data = json.loads(data)
            self.status = True           
                        
   def _players(self):
        for player in self._data:
            yield User(player)
                                   
   @property
   def online_players(self):
       return {'online': len(set(self._players)), 'max': self.max_slots}
                         
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
    
   #@property
   #def online_players(self):
   #      return f"{len(self.serverplayers)}/{self.max_players}"

   #@property 
   #def tags(self):
   #       tags = self.serverinfo_vars.get("tags")
   #       if tags:
   #           tags = list(tags.split(', '))
   #       else:
   #           tags = "This server has no tags."
   #       return tags

   #@property 
   #def top_tag(self):
   #        tags = self.tags
   #        if tags != "This server has no tags":
   #            toptag = tags[0]
   #        return toptag   

  #@property 
  #def version(self):
  #         return self.serverinfo.get("version", "No discord server was specified for this server.")     

  #property
  #def anticheat(self):
  #       return self.serverinfo_vars.get("Anticheat", "Disabled")   

  #@property
  #def community(self):
  #       eturn self.serverinfo_vars.get("Community", "No community server was specified for this server.")   


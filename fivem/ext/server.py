import asyncio
import json
import aiohttp
import re

from fivem.ext.user import User
from fivem.errors import BadIPFormat, ServerNotRespond
from fivem.ipformat import ServerIP

class FakeServer:
    __slots__ = ('srvip')

    def __init__(self, srvip):
        self.srvip = srvip
        self.status = False

    @property
    def queue(self):
         return []

    @property
    def players(self):
         return []

    @property
    def online_players(self):
         return (0, 0)

class Server:
         
    __slots__ = ('srvip', 'max_slots')

    def __new__(self, srvip: str, max_slots: int = 32):
        '''
        Server represents by FiveM Server Service
        `srvip` -> str       |   Server's IP
        `max_slots` -> int   |   Server's max players
        '''
        if self.check_server(srvip) is False:
             return FakeServer(srvip)
        else:
             self.srvip = srvip
        self.max_slots = max_slots 
        self.status = False

    def __repr__(self):
        return '<BetterFiveM-Service | <Server ip={0.srvip} status={0.status}' \
               ' online={1[0]}/{1[1]}>>'.format(self, self.online_players)

    def check_server(self, srvip):
        try:
             srvip = ServerIP().convert(srvip)
        except:
             return False
        else:
             return True

    async def get_players_data(self):
        async def fetch(session, mode):
            base_url = 'http://{}/{}.json'.format(self.srvip, mode)
            async with session.get(base_url) as resp:
                if resp.status != 200:
                    raise ServerNotRespond('[ERROR] Server is not responding or not found.')
                self.status = True
                return await resp.read() 

        async with aiohttp.ClientSession() as session:
            modes = ('players', 'info')                  
            for mode in modes:
                  fetched_data = await fetch(session, mode)
                  data = json.loads(fetched_data)
                  if mode == modes[0]: 
                       self.players_data = data   
                  elif mode == modes[1]:
                       self.info_data = data   
  
    @property
    def queue(self):
         pass
                                              
    @property
    def players(self):
        for player in self.players_data:
            yield User(player)

    @property
    def online_players(self):
        return (len(set(self.players)), self.max_slots)

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

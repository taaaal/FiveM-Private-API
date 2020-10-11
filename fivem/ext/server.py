import asyncio
import json
import aiohttp
import re
import socket

from fivem.ext.user import User
from fivem.errors import BadIPFormat, ServerNotRespond
from fivem.ipformat import ServerIP

class Server:
         
    def __init__(self, srvip: str, max_slots: int = 32):
        '''
        Server represents by FiveM Server Service
        `srvip` -> str       |   Server's IP
        `max_slots` -> int   |   Server's max players
        '''
        self.srvip = ServerIP().convert(srvip)
        self.max_slots = max_slots 

    def __repr__(self):
        return '<BetterFiveM-Service | <Server ip={0.srvip} status={0.status}' \
               ' online={1[0]}/{1[1]}>>'.format(self, self.online_players)

    async def get_players_data(self):
        async def fetch(session):
            async with session.get('http://{}/players.json'.format(self.srvip)) as resp:
                if resp.status != 200:
                    self.status = False
                    raise ServerNotRespond('[ERROR] Server is not responding or not found.')
                self.status = True
                return await resp.read() 

        async with aiohttp.ClientSession() as session:
            data = await fetch(session)    
            self._data = json.loads(data)         

    @property
    def players(self):
        for player in self._data:
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

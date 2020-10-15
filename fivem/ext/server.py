import asyncio
import json
import aiohttp
import re

from fivem.ext.user import User
from fivem.ext.fakeserver import FakeServer
from fivem.errors import BadIPFormat, ServerNotRespond
from fivem.ipformat import ServerIP

class Server:
    
    """
    Represent Online FiveM Server
    """
         
    __slots__ = ('_ip', '_max_players', '_status')

    def __new__(cls, ip, max_players=32):
        
        result = self.check_server_ip(ip) 
        if result is False:
            return FakeServer(ip)
            
        self = object.__new__(cls)
        self._ip = ip
        self._max_players = max_players 
        self._status = False
        return self
        
    def __repr__(self):
        return '<{0.__class__.__name__} ip={0.ip} status={0.status}' \
               ' online={1.online}/{1.max}>>'.format(self, self.sum_players)

    def check_server_ip(self, ip):
        try:
            ServerIP().convert(ip)
        except BadIPFormat:
            return False
        else:
            return True
            
    async def get_players_data(self):
        async def fetch(session, mode):
            base_url = 'http://{}/{}.json'.format(self.ip, mode)
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
    def ip(self):
         return self._ip
        
    @property
    def status(self):
         retrun self._status

    @property
    def max_players(self):
         return self._max_players
                                              
    @property
    def players(self):
        for player in self.players_data:
            yield User(player)

    @property
    def sum_players(self):
        _online = len(set(self.players))
        _max = self.max_players
        class OnlinePlayers:
            online = _online
            max = _max
        return OnlinePlayers
    
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

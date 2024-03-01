import asyncio
import json
import aiohttp

from fivem.ext.user import User
from fivem.ext.fakeserver import FakeServer
from fivem.errors import BadIPFormat, ServerNotRespond
from fivem.ipformat import ServerIP

class Server:
    
    """
    Represents Online FiveM Server
    """
         
    __slots__ = ('_ip', '_max_players', '_status')

    def __new__(cls, ip, max_players=32):
        
        result = self.check_server_ip(ip) 
        if not result:
            return FakeServer(ip)
            
        self = object.__new__(cls)
        self._ip = ip
        self._max_players = max_players 
        self._status = False
        return self
        
    def __repr__(self):
        return '<{0.__class__.__name__} ip={0.ip} status={0.status}' \
               ' online={1.online}/{1.max}>>'.format(self, self.players_count)

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
                self._status = True
                return await resp.read() 

        async with aiohttp.ClientSession() as session:
            fetched = await asyncio.gather(
                fetch(session, 'players'), 
                fetch(session, 'info')
            )
            
            self._players_data, self._info_data = map(json.loads, fetched)


    @property
    def ip(self):
         return self._ip
        
    @property
    def status(self):
         return self._status

    @property
    def max_players(self):
         return self._max_players
                                              
    @property
    def players(self):
        for player in self._players_data:
            yield User(player)

    @property
    def players_count(self):
        class OnlinePlayers:
            online = len(set(self.players))
            max    = self.max_players
        return OnlinePlayers

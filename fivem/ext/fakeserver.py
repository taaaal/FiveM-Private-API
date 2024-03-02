from fivem.utils import OnlinePlayers

class FakeServer:
    
    """
    Represents Offline FiveM Server
    """

    def __init__(self, ip):
        self._ip = ip
        self._max_players = 0
        self._status = False

    def __repr__(self):
        return '<{0.__class__.__name__} ip={0.ip} status={0.status}' \
               ' online={1.online}/{1.max}>'.format(self, self.players_count)

    @property
    def ip(self):
         return self._ip
         
    @property
    def max_players(self):
         return self._max_players        

    @property
    def status(self):
         return self._status

    @property
    def players(self):
         return []

    @property
    def players_count(self):
         return OnlinePlayers()

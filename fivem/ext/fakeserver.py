class FakeServer:
    
    """
    Represent Offline FiveM Server
    """

    def __init__(self, ip):
        self._ip = ip
        self._max_players = 0
        self._status = False

    def __repr__(self):
        return '<{0.__class__.__name__} ip={0.ip} status={0.status}' \
               ' online=0/0'.format(self)  

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
    def queue(self):
         return 0

    @property
    def players(self):
         return []

    @property
    def sum_players(self):
         class OnlinePlayers:
              online = 0
              max = 0
         return OnlinePlayers()

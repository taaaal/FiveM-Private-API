class CustomUsersSort:

    def __new__(cls, users, key='by_name', reversed=False):
        self = object.__new__(cls)
        self._users = users
        self._key = self.get_key(key)
        self._reversed = reversed
        return self.users

    @property    
    def users(self):
        new_sort = sorted(self._users, key=self._key, reversed=self._reversed)
        return new_sort
     
    def get_key(self, key):
        keys = {
            'by_name': self._by_name,
            'by_id'  : self._by_id,
            'by_ping': self._by_ping
        }
        return keys.get(key)

    def _by_name(self, user): 
        return ''.join(filter(str.isalpha, user.name)).lower()

    def _by_id(self, user):
        return user.id

    def _by_ping(self, user):
        return user.ping

class OnlinePlayers:
    
    def __init__(self, online, max):
        self.online = online
        self.max = max
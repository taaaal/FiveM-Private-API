import string

class CustomUsersSort:

    def __init__(self, users: list, key: str, reverse: bool = False):
        self._users = users
        self.key = self.get_key(key)
        self.reverse = reverse

    @property    
    def users(self):
        new_sort = sorted(self._users, key=self.key, reverse=self.reverse)
        return new_sort
     
    def get_key(self, key):
        keys = {
            'by_name': self.by_name,
            'by_id': self.by_id,
            'by_ping': self.by_ping
        }
        return keys.get(key)

    def by_name(self, user):
        leading_n = str()
        for n in user.name.lower():
            if n in string.ascii_lowercase:
                leading_n = n 
                break 
        return leading_n

    def by_id(self, user):
        return user.id

    def by_ping(self, user):
        return user.ping

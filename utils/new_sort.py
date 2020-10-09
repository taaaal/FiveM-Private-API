class CustomUsersSort:

    def init(self, users: list, key: str, reverse: bool = False):
        self._users = users
        self.key = self.get_key(key)
        self.reverse = reverse

    @property
    def users(self):
        new_users = sorted(self._users, key=self.key, reverse=self.reverse)
        return new_users

    def get_key(self, key):
        if key == 'by_name':
            key = self.by_name 
        elif key == 'by_id':
            key = self.by_id 
        elif key == 'by_ping':
            key = self.by_ping 
        return key

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

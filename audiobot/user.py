class User():
    def __init__(self, username):
        self.username = username


class DanmakuUser(User):
    def __init__(self, username, identifier, platform):
        super().__init__(username)
        self.identifier = identifier
        self.platform = platform


class SystemUser(User):
    def __init__(self, username="system"):
        super().__init__(username)


DefaultUser = SystemUser()
PlaylistUser = SystemUser(username="playlist")

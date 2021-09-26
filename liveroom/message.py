from audiobot.user import DanmakuUser


class DanmakuMessage():
    def __init__(self, user: DanmakuUser, message):
        self._user = user
        self._message = message

    @property
    def user(self) -> DanmakuUser:
        return self._user

    @property
    def message(self) -> str:
        return self._message

    @property
    def admin(self) -> bool:
        return False

    @property
    def privilege_level(self) -> int:
        return 0

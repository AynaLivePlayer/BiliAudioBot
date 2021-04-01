from pyncm import Session,SetCurrentSession


class pyncmpatchedSesion(Session):
    @classmethod
    def dopatch(cls):
        SetCurrentSession(cls())
    def update_headers(self):
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": self.UA_DEFAULT,
            "Referer": self.HOST,
            "X-Real-IP": "118.88.88.88"
        }
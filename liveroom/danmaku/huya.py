import asyncio

from audiobot.user import DanmakuUser
from liveroom.message import DanmakuMessage
from liveroom.platform import LivePlatform
from plugins import danmaku as dmk

from liveroom.danmaku import base


class HuyaLiveRoom(base.LiveRoom):

    def __init__(self, room_id):
        super().__init__()
        self._room_id = room_id
        self.q = asyncio.Queue()
        self.dmc = dmk.DanmakuClient("https://www.huya.com/{}".format(room_id), self.q)
        self.running = False

    @property
    def is_running(self) -> bool:
        return self.running

    def start(self):
        self.running = True
        self.loop.create_task(self.dmc.start())
        self.loop.create_task(self.__message_loop())


    def stop(self):
        self.running = False
        self.loop.create_task(self.dmc.stop())

    async def __message_loop(self):
        while self.running:
            m = await self.q.get()
            for handler in self.msg_handler.values():
                handler(HuyaDanmuMessage(m))

    @property
    def title(self):
        return ""

    @property
    def room_id(self):
        return self._room_id

    @property
    def unique_room_id(self):
        return "huya{}".format(self._room_id)

class HuyaDanmuMessage(DanmakuMessage):
    def __init__(self, message:dict):
        self.raw_message = message
        self._user = DanmakuUser(message["name"],"huya{}".format(message["name"]),LivePlatform.Huya)

    @property
    def user(self) -> DanmakuUser:
        return self._user

    @property
    def message(self) -> str:
        return self.raw_message["content"]

    @property
    def admin(self) -> bool:
        return False

    @property
    def privilege_level(self) -> int:
        return 0
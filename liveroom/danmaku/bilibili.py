import aiohttp

from audiobot.user import DanmakuUser
from liveroom.message import DanmakuMessage
from liveroom.platform import LivePlatform
from plugins import blivedm
from plugins.blivedm import DanmakuMessage as BliveMsg

from liveroom.danmaku import base

class BilibiliLiveRoom(base.LiveRoom):

    def __init__(self,room_id):
        super().__init__()
        self._room_id = room_id
        self.room = _DanmuClient(self._room_id,loop=self.loop)
        self.room._on_receive_danmaku = self._on_receive_danmaku

    @property
    def is_running(self) -> bool:
        return self.room.is_running

    def start(self):
        self.room.start()

    def stop(self):
        self.room.stop()

    @property
    def title(self):
        return self.room.title

    @property
    def room_id(self):
        return self._room_id

    @property
    def unique_room_id(self):
        return "bili{}".format(self._room_id)

    async def _on_receive_danmaku(self, msg: BliveMsg):
        for handler in self.msg_handler.values():
            handler(BiliDanmuMessage(msg))

class BiliDanmuMessage(DanmakuMessage):
    def __init__(self, message:BliveMsg):
        self.raw_message = message
        self._user = DanmakuUser(message.uname,message.uid,LivePlatform.Bilibili)

    @property
    def user(self) -> DanmakuUser:
        return self._user

    @property
    def message(self) -> str:
        return self.raw_message.msg

    @property
    def admin(self) -> bool:
        return bool(self.raw_message.admin)

    @property
    def privilege_level(self) -> int:
        # 舰队类型，0非舰队，1总督，2提督，3舰长
        return self.raw_message.privilege_type


class _DanmuClient(blivedm.BLiveClient):
    def __init__(self, room_id, uid=0, session: aiohttp.ClientSession = None, heartbeat_interval=30, ssl=True,loop=None):
        super().__init__(room_id, uid, session, heartbeat_interval, ssl, loop)

    @property
    def title(self):
        return self._title

    def _parse_room_init(self, data):
        super()._parse_room_init(data)
        room_info = data['room_info']
        self._title = room_info["title"]
        return True
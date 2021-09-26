import asyncio

# from liveroom import Global_Room_Manager

class LiveRoom():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.msg_handler = {}

    @classmethod
    def create(cls,room_id:str):
        from liveroom.danmaku.bilibili import BilibiliLiveRoom
        from liveroom.danmaku.huya import HuyaLiveRoom
        if room_id.startswith("bili"):
            return BilibiliLiveRoom(room_id[4:])
        if room_id.startswith("huya"):
            return HuyaLiveRoom(room_id[4:])
        return BilibiliLiveRoom(room_id)

    @property
    def title(self):
        return ""

    @property
    def room_id(self):
        return ""

    @property
    def unique_room_id(self):
        return ""

    @property
    def is_running(self) -> bool:
        return False

    def start(self):
        pass

    def stop(self):
        pass

    def register_msg_handler(self, handler_id, handler):
        self.msg_handler[handler_id] = handler

    def clear_msg_handler(self):
        self.msg_handler.clear()
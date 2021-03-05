import asyncio

import aiohttp

from plugins import blivedm
from plugins.blivedm import DanmakuMessage


class LiveRoom(blivedm.BLiveClient):
    def __init__(self, room_id, uid=0, session: aiohttp.ClientSession = None, heartbeat_interval=30, ssl=True,
                 loop=None):
        super().__init__(room_id, uid, session, heartbeat_interval, ssl, loop)
        self.msg_handler = {}

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def cover_url(self):
        return self._cover

    @property
    def cover(self):
        # todo media source
        return None

    def _parse_room_init(self, data):
        super()._parse_room_init(data)
        room_info = data['room_info']
        self._title = room_info["title"]
        self._cover = room_info["cover"]
        self._description = room_info["description"]
        return True

    async def _on_receive_danmaku(self, danmaku: DanmakuMessage):
        for handler in self.msg_handler.values():
            handler(danmaku)

    def registerMsgHandler(self, handler_id, handler):
        self.msg_handler[handler_id] = handler



# async def main():
#     # 参数1是直播间ID
#     # 如果SSL验证失败就把ssl设为False
#     room_id = 3819533
#     client = LiveRoom(room_id, ssl=True)
#     future = client.start()
#     try:
#         await future
#     finally:
#         await client.close()
#
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())
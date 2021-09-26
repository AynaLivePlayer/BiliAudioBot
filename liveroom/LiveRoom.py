# import asyncio
#
# import aiohttp
#
# from plugins import blivedm
# from plugins.blivedm import DanmakuMessage
# from sources.base import MediaSource
# from utils import vfile, vasyncio
#
# class LiveRoomA():
#     def __init__(self):
#         self.msg_handler = {}
#
#     @property
#     def title(self):
#         return ""
#
#     @property
#     def room_id(self):
#         return ""
#
#     @property
#     def unique_room_id(self):
#         return ""
#
#     def register_msg_handler(self, handler_id, handler):
#         self.msg_handler[handler_id] = handler
#
#     def clear_msg_handler(self):
#         self.msg_handler.clear()
#
#
# class LiveRoom(blivedm.BLiveClient):
#     def __init__(self, room_id, uid=0, session: aiohttp.ClientSession = None, heartbeat_interval=30, ssl=True,
#                  loop=None):
#         super().__init__(room_id, uid, session, heartbeat_interval, ssl, loop)
#         self.msg_handler = {}
#
#     @property
#     def title(self):
#         return self._title
#
#     @property
#     def description(self):
#         return self._description
#
#     @property
#     def cover_url(self):
#         return self._cover
#
#     @property
#     def cover(self):
#         # todo media source
#         suffix = vfile.getSuffixByUrl(self._cover)
#         return MediaSource(self._cover,
#                            {},
#                            "cover.{}".format(suffix))
#
#     def _parse_room_init(self, data):
#         super()._parse_room_init(data)
#         room_info = data['room_info']
#         self._title = room_info["title"]
#         self._cover = room_info["cover"]
#         self._description = room_info["description"]
#         return True
#
#     async def _on_receive_danmaku(self, danmaku: DanmakuMessage):
#         for handler in self.msg_handler.values():
#             asyncio.ensure_future(vasyncio.asyncwrapper(handler)(danmaku),loop=self._loop)
#
#     def registerMsgHandler(self, handler_id, handler):
#         self.msg_handler[handler_id] = handler
#
#     def clearMsgHandler(self):
#         self.msg_handler.clear()
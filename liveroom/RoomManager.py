import asyncio
from typing import Dict

from liveroom.LiveRoom import LiveRoom


def room_starter(liveroom: LiveRoom):
    async def wrapper():
        future = liveroom.start()
        try:
            await future
        finally:
            await liveroom.close()

    return wrapper


class RoomManager():
    def __init__(self, loop=None):
        self.loop = asyncio.get_event_loop() if loop == None else loop
        self.live_rooms: Dict[str, LiveRoom] = {}

    def count(self):
        return len(self.live_rooms.keys())

    def get_live_room_by_id(self, id):
        return self.live_rooms.get(id)

    def start_room(self, room_id):
        liveroom = self.live_rooms.get(room_id)
        if liveroom == None:
            return
        asyncio.ensure_future(room_starter(liveroom)())

    def get_running_room_ids(self):
        running = []
        for key, val in self.live_rooms.items():
            if val.is_running:
                running.append(key)
        return running

    def get_running_rooms(self):
        running = []
        for val in self.live_rooms.values():
            if val.is_running:
                running.append(val)
        return running

    def stop_room(self, room_id):
        return self.live_rooms.get(room_id) and self.live_rooms.get(room_id).stop()

    def stop_all(self):
        for val in self.live_rooms.values():
            if val.is_running:
                val.stop()

    def add_live_room(self, room_id) -> LiveRoom:
        if str(room_id) in self.live_rooms.keys():
            return self.live_rooms[str(room_id)]
        liveroom = LiveRoom(room_id, uid=208259, loop=self.loop)
        self.live_rooms[str(room_id)] = liveroom
        return liveroom

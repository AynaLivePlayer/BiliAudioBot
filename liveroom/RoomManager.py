import asyncio
from typing import Dict

from liveroom.LiveRoom import LiveRoom

def room_starter(liveroom:LiveRoom):
    async def wrapper():
        future = liveroom.start()
        try:
            await future
        finally:
            await liveroom.close()
    return wrapper

class RoomManager():
    def __init__(self):
        self.live_rooms:Dict[str,LiveRoom] = {}

    def count(self):
        return len(self.live_rooms.keys())

    def getLiveRoomById(self,id):
        return self.live_rooms.get(id)

    def startRoom(self,room_id):
        liveroom = self.live_rooms.get(room_id)
        if liveroom == None:
            return
        asyncio.gather(room_starter(liveroom)())


    def stopRoom(self,room_id):
        return self.live_rooms.get(room_id) and self.live_rooms.get(room_id).stop()

    def addLiveRoom(self,room_id) -> LiveRoom:
        liveroom = LiveRoom(room_id,uid = 208259)
        self.live_rooms[str(room_id)] = liveroom
        return liveroom

print("Initialize global room manager")
Global_Room_Manager = RoomManager()
# if __name__ == '__main__':
#     GlobalRoomManager.startRoom("3819533")
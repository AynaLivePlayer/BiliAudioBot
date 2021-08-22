from audiobot import Global_Audio_Bot
from audiobot.event.audiobot import AudioBotStartEvent
from liveroom import Global_Room_Manager
from config import Config

@Global_Audio_Bot.handlers.register(AudioBotStartEvent,
                                    "addon.connect_when_start")
def connect_when_start(event: AudioBotStartEvent):
    if Config.default_room != "":
        Global_Room_Manager.stop_all()
        lr = Global_Room_Manager.add_live_room(Config.default_room)
        Global_Room_Manager.start_room(Config.default_room)
        Global_Audio_Bot.setLiveRoom(lr)
        print("live room connected")


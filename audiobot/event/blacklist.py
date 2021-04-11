from audiobot.event.base import BaseAudioBotEvent

class BlacklistUpdateEvent(BaseAudioBotEvent):
    __event_name__ = "blacklist_update"

    def __init__(self, blacklist):
        self.blacklist = blacklist



class BlacklistLoadedEvent(BaseAudioBotEvent):
    __event_name__ = "blacklist_loaded"

    def __init__(self, blacklist):
        self.blacklist = blacklist
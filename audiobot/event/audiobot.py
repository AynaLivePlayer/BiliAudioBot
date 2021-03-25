from audiobot.event.base import BaseAudioBotEvent, CancellableEvent


class AudioBotPlayEvent(BaseAudioBotEvent):
    __event_name__ = "audiobot_play"

    def __init__(self, audio_bot, item):
        self.audio_bot = audio_bot
        self.item = item


class FindSearchResultEvent(BaseAudioBotEvent,
                            CancellableEvent):
    def __init__(self,  search_result):
        self.search_result = search_result
        self.cancelled = False

    def isCancelled(self):
        return self.cancelled

    def setCancelled(self, b):
        self.cancelled = b
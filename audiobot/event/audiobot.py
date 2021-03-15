from audiobot.event.base import BaseAudioBotEvent


class AudioBotPlayEvent(BaseAudioBotEvent):
    __event_name__ = "audiobot_play"

    def __init__(self, audio_bot, item):
        self.audio_bot = audio_bot
        self.item = item
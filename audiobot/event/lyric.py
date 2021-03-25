from audiobot.event.base import BaseAudioBotEvent


class LyricUpdateEvent(BaseAudioBotEvent):
    __event_name__ = "lyric_update"

    def __init__(self, lyrics, lyric):
        self.lyrics = lyrics
        self.lyric = lyric

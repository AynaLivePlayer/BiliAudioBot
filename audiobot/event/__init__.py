from audiobot.event.audiobot import AudioBotPlayEvent
from audiobot.event.playlist import PlaylistAppendEvent


class AudioBotEvents():
    AUDIOBOT_PLAY = AudioBotPlayEvent
    PLAYLIST_APPEND = PlaylistAppendEvent

    values = [AUDIOBOT_PLAY,PLAYLIST_APPEND]
    names = [x.__event_name__ for x in values]

    @classmethod
    def getByName(cls,name):
        for e in cls.values:
            if name == e.__event_name__:
                return e
        return None
from sources.base import CommonSource, TextSource


class AudioSource(CommonSource):
    __source_name__ = "base"

    @classmethod
    def getSourceName(cls):
        return "audio.%s" % cls.__source_name__

    @property
    def audio(self):
        return None

    @property
    def lyric(self) -> TextSource:
        return None

from .netease import NeteaseMusicSource
from .bilibili import BiliAudioSource
from .kuwo import KuwoMusicSource
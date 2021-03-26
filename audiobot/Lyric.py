import asyncio
import re
import traceback
import aiohttp
from typing import List

from audiobot.Handler import AudioBotHandlers
from audiobot.Playlist import PlaylistItem
from audiobot.event.lyric import LyricUpdateEvent
from sources.audio import AudioSource


class LyricItem():
    @staticmethod
    def convertToSec(raw):
        raw = raw[1:-1:].split(":")
        minutes = raw[0]
        seconds = raw[1]
        return float(minutes) * 60 + float(seconds)

    def __init__(self, time, lyric):
        self.time = time
        self.lyric = lyric

    @classmethod
    def initFromRaw(cls, text):
        time_pattern = re.compile(r"\[[0-9]+:[0-9]+\.[0-9]+\]")
        tt = time_pattern.match(text)
        if tt is None:
            return None
        try:
            return cls(cls.convertToSec(tt.group()), time_pattern.sub("", text))
        except:
            traceback.print_exc()
            return None


class Lyrics():
    def __init__(self, audiobot):
        self.audiobot = audiobot
        self.lyrics: List[LyricItem] = []
        self.previous = None
        self.handlers = AudioBotHandlers()

    def load(self, item: PlaylistItem):
        self.clear()
        source = item.source
        if not isinstance(source,AudioSource):
            return
        else:
            lrc_source = source.lyric
        if lrc_source is None:
            return
        if lrc_source.filecontent != "":
            self.loadContent(lrc_source.filecontent)
        else:
            asyncio.ensure_future(self._async_load(lrc_source), loop=self.audiobot._loop)

    async def _async_load(self,lrc_source):
        async with aiohttp.ClientSession() as session:
            async with session.get(lrc_source.url, headers=lrc_source.headers) as response:
                self.loadContent(await response.text())

    def loadContent(self, raw):
        for line in raw.split("\n"):
            li = LyricItem.initFromRaw(line)
            if li is not None:
                self.lyrics.append(li)
        self.lyrics.append(LyricItem(2147483647, ""))

    def findLyricByTime(self, time):
        for i in range(len(self.lyrics) - 1):
            if (self.lyrics[i].time <= time < self.lyrics[i + 1].time):
                return self.lyrics[i]
            else:
                continue


    def clear(self):
        self.handlers.call(LyricUpdateEvent(self,
                                            LyricItem(0,"")))
        self.lyrics.clear()

    def _raiseEvent(self,property,val,*args):
        if val is None:
            return
        lrc = self.findLyricByTime(float(val))
        if lrc is None:
            return
        if self.previous and lrc.lyric == self.previous.lyric:
            return
        self.previous = lrc
        self.handlers.call(LyricUpdateEvent(self,
                                            self.findLyricByTime(int(val))))
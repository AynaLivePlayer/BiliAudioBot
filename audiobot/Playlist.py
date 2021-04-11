from typing import List, Type, Union

from audiobot.Handler import AudioBotHandlers
from audiobot.event.base import BaseAudioBotEvent
from audiobot.event.playlist import PlaylistUpdateEvent, PlaylistAppendEvent
from sources.base import CommonSource
from functools import wraps

from sources.base.interface import AudioBotInfoSource
import random


# def executeHandler(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         retval = func(self, *args, **kwargs)
#         self._callHandlers()
#         return retval
#     return wrapper


def triggerEventHandler(func):
    @wraps(func)
    def executeHandler(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        if ret is None:
            return
        if isinstance(ret,BaseAudioBotEvent):
            retval, event = None, ret
        else:
            retval, event = ret[0], ret[1]
        self.handlers.call(event)
        return retval

    return executeHandler


class PlaylistItem():
    def __init__(self, source: Union[CommonSource, AudioBotInfoSource], username, keyword):
        self.source = source
        self.username = username
        self.keyword = keyword


class Playlist():
    def __init__(self, audio_bot, name,random_next=False):
        self.audio_bot = audio_bot
        self.name = name
        self.playlist: List[PlaylistItem] = []
        self.current_index = 0
        self.handlers = AudioBotHandlers()
        self.random_next = random_next

    def __len__(self):
        return len(self.playlist)

    def size(self):
        return len(self.playlist)

    def append(self, cm, username="system", keyword=""):
        return self.appendItem(PlaylistItem(cm, username, keyword))

    def appendItem(self, item: PlaylistItem):
        event = PlaylistAppendEvent(self, item)
        self.handlers.call(event)
        if event.isCancelled():
            return event
        self.playlist.append(item)
        self.handlers.call(PlaylistUpdateEvent(self))
        return event

    def get(self, index):
        if index >= len(self.playlist) or index < 0:
            return
        return self.playlist[index]

    def clear(self):
        self.playlist.clear()
        self.handlers.call(PlaylistUpdateEvent(self))

    @triggerEventHandler
    def popFirst(self):
        if len(self.playlist) == 0:
            return None
        return self.playlist.pop(0), PlaylistUpdateEvent(self)

    @triggerEventHandler
    def remove(self, index):
        if index >= len(self.playlist) or index < 0:
            return
        return self.playlist.pop(index), PlaylistUpdateEvent(self)

    @triggerEventHandler
    def move(self, index, target_index):
        if index >= len(self.playlist) or index < 0:
            return
        if target_index < 0:
            target_index = 0
        if target_index >= len(self.playlist):
            target_index = len(self.playlist) - 1
        if index == target_index:
            return
        step = int((target_index - index) / abs(target_index - index))
        tmp = self.playlist[index]
        for i in range(index, target_index, step):
            self.playlist[i] = self.playlist[i + step]
        self.playlist[target_index] = tmp
        return PlaylistUpdateEvent(self)

    def getNext(self):
        if len(self.playlist) == 0:
            return
        if self.random_next:
            self.current_index = random.randint(0, len(self.playlist) - 1)
            return self.playlist[self.current_index]
        if self.current_index >= len(self.playlist):
            self.current_index = 0
        self.current_index += 1
        return self.playlist[self.current_index - 1]
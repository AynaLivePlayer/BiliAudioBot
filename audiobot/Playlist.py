from typing import List, Type, Union

from audiobot.event.base import BaseAudioBotEvent
from audiobot.event.playlist import PlaylistUpdateEvent, PlaylistAppendEvent
from sources.base import CommonSource
from functools import wraps

from sources.base.interface import AudioBotInfoSource
import random


def executeHandler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        retval = func(self, *args, **kwargs)
        self._callHandlers()
        return retval

    return wrapper


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
        self._callHandlers(event)
        return retval

    return executeHandler


class PlaylistItem():
    def __init__(self, source: Union[CommonSource, AudioBotInfoSource], username, keyword):
        self.source = source
        self.username = username
        self.keyword = keyword


class Playlist():
    def __init__(self, audio_bot, random_next=False):
        self.audio_bot = audio_bot
        self.playlist: List[PlaylistItem] = []
        self.current_index = 0
        self._event_handlers = {}
        self.random_next = random_next

    def __len__(self):
        return len(self.playlist)

    def size(self):
        return len(self.playlist)


    def append(self, cm, username="system", keyword=""):
        self.appendItem(PlaylistItem(cm, username, keyword))

    @triggerEventHandler
    def appendItem(self, item: PlaylistItem):
        event = PlaylistAppendEvent(self, item)
        self._callHandlers(event)
        if event.isCancelled():
            return
        self.playlist.append(item)
        return PlaylistUpdateEvent(self)

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

    @triggerEventHandler
    def getNext(self):
        if len(self.playlist) == 0:
            return
        if self.random_next:
            return self.playlist[random.randint(0, len(self.playlist) - 1)], PlaylistUpdateEvent(self)
        if self.current_index >= len(self.playlist):
            self.current_index = 0
        self.current_index += 1
        return self.playlist[self.current_index - 1], PlaylistUpdateEvent(self)

    def _callHandlers(self, event: BaseAudioBotEvent):
        event_name: str = event.__event_name__
        if self._event_handlers.get(event_name) is None:
            return
        for func in self._event_handlers.get(event_name).values():
            func(event)

    def registerHandler(self, event_name, id, func):
        if self._event_handlers.get(event_name) is None:
            self._event_handlers[event_name] = {}
        self._event_handlers[event_name][id] = func

    def unregisterEventHanlder(self, event_name, id):
        try:
            self._event_handlers.get(event_name).pop(id)
        except:
            pass

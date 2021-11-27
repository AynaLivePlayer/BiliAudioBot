from typing import List

from audiobot.audio import AudioItem
from audiobot.handler import AudioBotHandlers
from audiobot.event.base import BaseAudioBotEvent
from audiobot.event.playlist import PlaylistUpdateEvent, PlaylistAppendEvent
from functools import wraps

import random
from audiobot.user import User, PlaylistUser


def _trigger_event_handler(func):
    @wraps(func)
    def execute_handler(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        if ret is None:
            return
        if isinstance(ret, BaseAudioBotEvent):
            retval, event = None, ret
        else:
            retval, event = ret[0], ret[1]
        self.handlers.call(event)
        return retval
    return execute_handler


class Playlist():
    def __init__(self, audio_bot, name, random_next=False):
        self.audio_bot = audio_bot
        self.name = name
        self.playlist: List[AudioItem] = []
        self.current_index = 0
        self.handlers = AudioBotHandlers()
        self.random_next = random_next

    def __len__(self):
        return len(self.playlist)

    def size(self):
        return len(self.playlist)

    def insert_raw(self, cm, index, user: User = None, keyword="") -> PlaylistAppendEvent:
        event = self.append_raw(cm, user=user, keyword=keyword)
        if event.isCancelled():
            return event
        self.move(event.index, index)
        return event

    def append_raw(self, cm, user: User = None, keyword="") -> PlaylistAppendEvent:
        if user is None:
            return self.append(AudioItem(cm, PlaylistUser, keyword))
        else:
            return self.append(AudioItem(cm, user, keyword))

    def insert(self, index: int, item: AudioItem) -> PlaylistAppendEvent:
        event = self.append(item)
        if event.isCancelled():
            return event
        self.move(event.index, index)
        return event

    def append(self, item: AudioItem) -> PlaylistAppendEvent:
        event = PlaylistAppendEvent(self, item, self.size())
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

    @_trigger_event_handler
    def pop_first(self):
        if len(self.playlist) == 0:
            return None
        return self.playlist.pop(0), PlaylistUpdateEvent(self)

    @_trigger_event_handler
    def remove(self, index):
        if index >= len(self.playlist) or index < 0:
            return
        return self.playlist.pop(index), PlaylistUpdateEvent(self)

    @_trigger_event_handler
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

    def get_next(self) -> AudioItem:
        '''
        get next AudioItem, if not exists return None

        :return: AudioItem
        '''
        if len(self.playlist) == 0:
            return
        index = 0
        if self.random_next:
            index = random.randint(0, len(self.playlist) - 1)
            self.current_index = index
        else:
            index = self.current_index
            self.current_index += 1
            if self.current_index >= self.size():
                self.current_index = 0
        self.playlist.sort()
        return self.playlist[index]

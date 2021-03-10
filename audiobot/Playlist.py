
from typing import List, Type, Union

from sources.base import CommonSource
from functools import wraps

from sources.base.interface import AudioBotInfoSource
import random

def executeHandler(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        retval = func(self,*args,**kwargs)
        self._callHandlers()
        return retval
    return wrapper

class PlaylistItem():
    def __init__(self,source:Union[CommonSource,AudioBotInfoSource],username,keyword):
        self.source = source
        self.username = username
        self.keyword = keyword

class Playlist():
    def __init__(self,audio_bot,random_next = False):
        self.audio_bot =audio_bot
        self.playlist:List[PlaylistItem] = []
        self.current_index = 0
        self.handlers = {}
        self.random_next = random_next

    def __len__(self):
        return len(self.playlist)

    def size(self):
        return len(self.playlist)

    @executeHandler
    def append(self,cm,username="system",keyword=""):
        self.playlist.append(PlaylistItem(cm,username,keyword))

    @executeHandler
    def appendItem(self, item:PlaylistItem):
        self.playlist.append(item)

    @executeHandler
    def popFirst(self):
        if len(self.playlist) == 0:
            return None
        return self.playlist.pop(0)

    @executeHandler
    def remove(self,index):
        if index >= len(self.playlist) or index < 0:
            return
        return self.playlist.pop(index)

    @executeHandler
    def move(self, index,target_index):
        if index >= len(self.playlist) or index < 0:
            return
        if target_index < 0:
            target_index = 0
        if target_index >= len(self.playlist):
            target_index = len(self.playlist) - 1
        if index == target_index:
            return
        step = int((target_index - index) / abs(target_index-index))
        tmp = self.playlist[index]
        for i in range(index,target_index,step):
            self.playlist[i] = self.playlist[i+step]
        self.playlist[target_index] = tmp

    @executeHandler
    def getNext(self):
        if len(self.playlist) == 0:
            return None
        if self.random_next:
            return self.playlist[random.randint(0,len(self.playlist)-1)]
        if self.current_index >= len(self.playlist):
            self.current_index = 0
        self.current_index +=1
        return self.playlist[self.current_index-1]

    def _callHandlers(self):
        for val in self.handlers.values():
            self.audio_bot._async_call(val,self)

    def registerHandler(self,id,func):
        self.handlers[id] = func
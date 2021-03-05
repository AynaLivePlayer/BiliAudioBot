from typing import List

from sources.base import CommonSource
from functools import wraps

def executeHandler(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        retval = func(self,*args,**kwargs)
        self.__callHandlers()
        return retval
    return wrapper

class Playlist():
    def __init__(self):
        self.playlist:List[CommonSource] = []
        self.current_index = 0
        self.handlers = {}

    def __len__(self):
        return len(self.playlist)

    def size(self):
        return len(self.playlist)

    @executeHandler
    def append(self,cm):
        self.playlist.append(cm)

    @executeHandler
    def popFirst(self):
        if len(self.playlist) == 0:
            return None
        return self.playlist.pop(0)

    @executeHandler
    def getNext(self):
        if len(self.playlist) == 0:
            return None
        if self.current_index >= len(self.playlist):
            self.current_index = 0
        self.current_index +=1
        return self.playlist[self.current_index-1]

    def _callHandlers(self):
        for val in self.handlers.values():
            val(self)

    def registerHandler(self,id,func):
        self.handlers[id] = func
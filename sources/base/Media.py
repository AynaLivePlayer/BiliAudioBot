
from sources.base import BaseSource
from sources.base.interface import WatchableSource
from utils import formats,vfile
import os

class MediaSource(BaseSource,WatchableSource):
    __source_name__ = "media"

    def __init__(self,url,headers,filename):
        self.url = url
        self.headers = headers
        self.filename = filename

    @property
    def suffix(self):
        return self.filename.split(".")[-1]

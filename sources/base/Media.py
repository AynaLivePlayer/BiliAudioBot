
from sources.base import BaseSource
from utils import formats,file
import os

class MediaSource(BaseSource):
    __source_name__ = "media"

    def __init__(self,url,headers,filename):
        self.url = url
        self.headers = headers
        self.filename = filename

    @property
    def suffix(self):
        return self.filename.split(".")[-1]

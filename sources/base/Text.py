from sources.base.interface import DownloadableSource
from utils import vfile

from sources.base import BaseSource


class TextSource(BaseSource):
    __source_name__ = "text"

    def __init__(self, url, headers, filename, filecontent):
        self.url = url
        self.headers = headers
        self.filename = filename
        self.filecontent = filecontent

    @property
    def suffix(self):
        return self.filename.split(".")[-1]
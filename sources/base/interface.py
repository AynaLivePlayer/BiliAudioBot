from abc import ABCMeta, abstractmethod

from sources.base.Picture import PictureSource
from sources.base.SearchResult import SearchResults


class BaseInterface(metaclass=ABCMeta):
    pass


class DownloadableSource(BaseInterface):
    @abstractmethod
    def download(self, downloader, saveroute, **kwargs):
        pass

    @property
    @abstractmethod
    def suffix(self):
        return ""


class SearchableSource(BaseInterface):
    @classmethod
    @abstractmethod
    def search(cls, keyword, *args, **kwargs) -> SearchResults:
        pass


class WatchableSource(BaseInterface):
    pass

class AudioBotInfoSource():
    @abstractmethod
    def getUniqueId(self):
        return None

    @abstractmethod
    def getTitle(self):
        return None

    @abstractmethod
    def getArtist(self):
        return None

    @abstractmethod
    def getCover(self) -> PictureSource:
        return None

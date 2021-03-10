import re

from apis import RegExpResponseContainer, JsonResponseContainer
from sources.audio import AudioSource
from sources.base import SearchResults, CommonSourceWrapper, MediaSource, SearchResult, PictureSource
from sources.base.interface import SearchableSource, AudioBotInfoSource
from apis import kuwo as kuwoApi
from utils import file


class KuwoMusicSource(AudioSource,
                      AudioBotInfoSource,
                      SearchableSource):

    __source_name__ = "kuwo"
    pattern = "kuwo[0-9]+"

    def __init__(self,id):
        self.id = id
        self.artist = ""
        self.title = ""

    @classmethod
    def search(cls, keyword, page=1, pagesize=20, *args, **kwargs) -> SearchResults:
        try:
            container = JsonResponseContainer(kuwoApi.getSearchResult(keyword,
                                                                      page=page,
                                                                      pagesize=pagesize),
                                              total = ("data.total",int),
                                              songlist="data.list")
            rs = []
            for song in container.data["songlist"]:
                id = song["musicrid"].replace("MUSIC_", "")
                source = cls(id)
                source.title = song["name"]
                source.artist = song["artist"]
                rs.append(SearchResult(kuwoApi.API.info_url(id),
                                       {},
                                       "{} - {}".format(song["name"],
                                                        song["artist"]
                                                        ),
                                       source,
                                       cls.getSourceName(),
                                       "audio"))
            return SearchResults(rs,1,container.data["total"] // pagesize)
        except:
            return SearchResults([], 0, 0)

    @property
    def audio(self):
        return self.getAudio()

    @CommonSourceWrapper.handleException
    def getAudio(self):
        url = kuwoApi.getMusicFile(self.id).decode()
        return MediaSource(url,
                           kuwoApi.API.file_headers,
                           "{} - {}.{}".format(self.title,
                                               self.artist,
                                               file.getSuffixByUrl(url)))

    def getTitle(self):
        return self.title

    def getArtist(self):
        return self.artist

    def getCover(self) -> PictureSource:
        return None

    @classmethod
    def initFromUrl(cls, url:str):
        if url.isdigit():
            return cls(url)
        r = re.search(cls.pattern,url)
        return cls(r.group()[4::]) if r != None else None

    @property
    def info(self):
        return {"Type": self.getBaseSources(),
                "ID": self.id,
                "Title": self.title,
                "Artist": self.artist}

    def getBaseSources(self, *args, **kwargs):
        return {"audio": self.getAudio()}

    @CommonSourceWrapper.handleException
    def load(self, *args, **kwargs):
        if self.isValid():
            return
        title = RegExpResponseContainer(kuwoApi.getMusicInfo(self.id),
                                        title=(r"<title>(.*)</title>",
                                               lambda x: x[7:-8:].split("_")))
        self.title = title.data["title"][0]
        self.artist = title.data["title"][1]

    @classmethod
    def applicable(cls, url):
        return re.search(cls.pattern,url) != None

    def isValid(self):
        return self.artist != "" and self.title != ""

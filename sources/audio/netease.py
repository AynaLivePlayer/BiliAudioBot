import re

from config import Config
from sources.base import SearchResults, MediaSource, SearchResult, CommonSourceWrapper, PictureSource, TextSource
from sources.audio import AudioSource
from sources.base.interface import SearchableSource, AudioBotInfoSource
from pyncm.apis import track,cloudsearch,playlist

from utils import vfile

class NeteaseMusicSource(AudioSource,
                         SearchableSource,
                         AudioBotInfoSource):
    __source_name__ = "netease-audio"

    base_url = "https://music.163.com/"

    song_url = "https://music.163.com/#/song?id={id}"

    pattern = r"music\.163\.com/\#/song\?id=[0-9]+"
    patternB = r"163audio[0-9]+"
    patternC = r"wy[0-9]+"

    @classmethod
    def addXRealIP(cls,header):
        h = header.copy()
        h["X-Real-IP"] = "118.88.88.88"
        return h

    @classmethod
    def search(cls, keyword, pagesize=10,*args, **kwargs) -> SearchResults:
        data = cloudsearch.GetSearchResult(keyword,limit=pagesize,offset=0)
        if data["result"]["songCount"] == 0:
            return SearchResults([],0,0)
        results = []
        for song in data["result"]["songs"]:
            ns = cls(song["id"])
            ns.cover_url = song["al"]["picUrl"]
            ns.artists = [ar["name"] for ar in song["ar"]]
            ns.vip = bool(song["fee"])
            ns.title = song["name"]
            results.append(SearchResult(cls.song_url.format(id=song["id"]),
                                        {},
                                        ns._getParsedTitle(),
                                        ns,
                                        cls.getSourceName(),
                                        "audio"))
        return SearchResults(results,1,1)

    def __init__(self,sid):
        self.sid = sid
        self.cover_url = ""
        self.artists = []
        self.title = ""
        self.vip = False
        self.available = False

    def getTitle(self):
        return self.title

    def getArtist(self):
        return ",".join(self.artists)

    def getCover(self) -> PictureSource:
        if self.cover_url != "":
            suffix = vfile.getSuffixByUrl(self.cover_url)
            return PictureSource(self.cover_url, {}, ".".join([self.title, suffix]), "")
        return None

    @property
    def lyric(self):
        return self.getLyric()

    def getLyric(self):
        data = track.GetTrackLyrics(self.sid)
        if data.get("lrc") is not None:
            return TextSource("",{},"{}.lrc".format(self._getParsedTitle()),
                              data["lrc"]["lyric"])
        return
    @property
    def audio(self):
        return self.getAudio()

    @CommonSourceWrapper.handleException
    def getAudio(self):
        data = track.GetTrackAudio(self.sid)
        url = data["data"][0]["url"]
        if url == None:
            return None
        return MediaSource(data["data"][0]["url"],
                           self.addXRealIP(Config.commonHeaders),
                           "{}.{}".format(self._getParsedTitle(), vfile.getSuffixByUrl(url)))

    def isValid(self):
        return self.sid != "" and self.title != ""

    @classmethod
    def initFromUrl(cls, url:str):
        if (url.isdigit()):
            return cls(url)
        id = re.search(r"id=[0-9]+",url)
        if id != None: return cls(id.group()[3::])
        id = re.search(cls.patternB, url)
        if id != None: return cls(id.group()[8::])
        id = re.search(cls.patternC, url)
        if id != None: return cls(id.group()[2::])
        return None

    @property
    def info(self):
        return {"Type": self.getSourceName(),
                "Title": self.title,
                "Vip": "Yes" if self.vip else "No",
                "Artists": ",".join(self.artists)}

    def getBaseSources(self,*args,**kwargs):
        return {"audio":self.getAudio()}

    @CommonSourceWrapper.handleException
    def load(self,*args,**kwargs):
        data = track.GetTrackDetail(self.sid)
        self.artists = [ar["name"] for ar in data["songs"][0]["ar"]]
        self.cover_url = data["songs"][0]["al"]["picUrl"]
        audiodata = track.GetTrackAudio(self.sid)["data"][0]
        self.vip = audiodata["freeTrialInfo"] != None
        self.available = audiodata["url"] != None
        self.title = data["songs"][0]["name"]

    @classmethod
    def applicable(cls, url):
        return re.search(cls.pattern,url) != None or \
               re.search(cls.patternB,url) != None or \
               re.search(cls.patternC,url) != None

    def _getParsedTitle(self):
        return "{title} - {artists}".format(title = self.title,
                                            artists = ",".join(self.artists))


class NeteasePlaylistSource(AudioSource):
    __source_name__ = "netease-list"

    pattern = r"wypl[0-9]+"

    def __init__(self, pid):
        self.playlist_id = pid
        self.audios = []

    @property
    def id(self):
        return self.playlist_id

    @property
    def info(self):
        return {"Type": self.getSourceName(),
                "Audio number": len(self.audios)}

    @classmethod
    def applicable(cls, url):
        return re.search(cls.pattern, url) != None

    @classmethod
    def initFromUrl(cls, url:str):
        if url.isdigit():
            return cls(url)
        rs = re.search(cls.pattern, url)
        return cls(rs.group()[4::]) if rs != None else None

    @CommonSourceWrapper.handleException
    def load(self,*args,**kwargs):
        self.audios.clear()
        trackids = playlist.GetPlaylistInfo(self.playlist_id)["playlist"]["trackIds"]
        for track in trackids:
            self.audios.append(NeteaseMusicSource(str(track["id"])))

    def getBaseSources(self,**kwargs):
        if not self.isValid(): return {}
        audio: NeteaseMusicSource
        return {"audio":[audio.getBaseSources(**kwargs) for audio in self.audios]}

    def isValid(self):
        return True if len(self.audios) > 0 else False


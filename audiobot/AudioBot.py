from typing import List, Type

from audiobot.Playlist import Playlist
from liveroom.LiveRoom import LiveRoom
from player.mpv import MPVPlayer, MPVProperty
from plugins.blivedm import DanmakuMessage
from sources.audio import NeteaseMusicSource,BiliAudioSource
from sources.base import CommonSource, BaseSource, SourceSelector
from sources.base.interface import WatchableSource, SearchableSource
from sources.video.bilibili import BiliVideoSource


class AudioBot():
    selector = SourceSelector(NeteaseMusicSource,
                              BiliAudioSource,
                              BiliVideoSource)

    def __init__(self):
        self.user_playlist = Playlist()
        self.system_playlist = Playlist()
        self.current:CommonSource = None
        self.mpv_player: MPVPlayer = None
        self.live_room:LiveRoom = None

    def setPlayer(self,mpv_player: MPVPlayer):
        self.mpv_player = mpv_player
        self.mpv_player.registerPropertyHandler("audiobot.idleplaynext",
                                                MPVProperty.IDLE,
                                                self.__idle_play_next)

    def setLiveRoom(self,live_room:LiveRoom):
        if self.live_room != None:
            self.live_room.clearMsgHandler()
        self.live_room = live_room
        self.live_room.registerMsgHandler("audiobot.msg",
                                          self.__danmu_add_playlist)

    def __getPlayableSource(self,sources:dict) -> BaseSource:
        for val in sources.values():
            val:BaseSource
            if isinstance(val,WatchableSource) and isinstance(val,BaseSource):
                return val
        return None

    def __chooseNext(self):
        if self.system_playlist.size() == 0:
            return
        return self.system_playlist.getNext()

    def playNext(self):
        if len(self.user_playlist) == 0 and len(self.system_playlist) == 0:
            return
        if len(self.user_playlist) != 0:
            self.__play(self.user_playlist.popFirst().source)
            return
        if len(self.user_playlist) != 0:
            self.__play(self.__chooseNext().source)

    def __play(self,source:CommonSource):
        bs:BaseSource = self.__getPlayableSource(source.getBaseSources())
        if bs == None:
            return
        self.current = source
        self.mpv_player.playByUrl(bs.url, headers=bs.headers)

    def addAudioByUrl(self,url,username="system",source:Type[CommonSource.__class__]=None):
        source:CommonSource.__class__ = source if source else self.selector.select(url)
        if source != None:
            cm: CommonSource = source.initFromUrl(url)
            if cm == None and issubclass(source, SearchableSource):
                srs = source.search(url)
                if srs.isEmpty():
                    return
                cm = srs.results[0].source
        else:
            srs = NeteaseMusicSource.search(url)
            if srs.isEmpty():
                return
            cm = srs.results[0].source
        if cm == None:
            return
        cm.load()
        if cm.isValid():
            self.user_playlist.append(cm,username=username)
        if self.mpv_player.getProperty(MPVProperty.IDLE):
            self.playNext()

    def __danmu_add_playlist(self,dmkMsg:DanmakuMessage,*args, **kwargs):
        msg:str = dmkMsg.msg.split(" ")
        if len(msg) < 2:
            return
        hintword,val = msg[0]," ".join(msg[1::])
        if (hintword == "点歌"):
            self.addAudioByUrl(val,username=dmkMsg.uname)
        elif hintword == "点b歌":
            self.addAudioByUrl(val,username=dmkMsg.uname,source=BiliAudioSource)
        elif hintword == "点w歌":
            self.addAudioByUrl(val,username=dmkMsg.uname,source=NeteaseMusicSource)

    def __idle_play_next(self,prop,value, *args, **kwargs):
        if value:
            self.current = None
            self.playNext()


print("Initialize global audio bot")
Global_Audio_Bot = AudioBot()

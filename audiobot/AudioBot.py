from typing import List

from gui import MPVGUI
from liveroom.LiveRoom import LiveRoom
from player.mpv import MPVPlayer, MPVProperty
from plugins.blivedm import DanmakuMessage
from sources.audio.netease import NeteaseMusicSource
from sources.base import MediaSource, CommonSource, BaseSource
from sources.base.interface import WatchableSource


class AudioBot():
    def __init__(self):
        self.user_playlist: List[CommonSource] = []
        self.system_playlist: List[CommonSource] = []
        self.system_playlist_index = 0
        self.current:CommonSource = None
        self.mpv_player: MPVPlayer = None
        self.live_room:LiveRoom = None

    def setPlayer(self,mpv_player):
        self.mpv_player = mpv_player
        self.mpv_player.registerPropertyHandler("audiobot.idleplaynext",
                                                MPVProperty.IDLE,
                                                self.__idle_play_next)

    def setLiveRoom(self,live_room:LiveRoom):
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
        if self.system_playlist_index >= len(self.system_playlist):
            self.system_playlist_index = 0
        self.system_playlist_index +=1
        return self.system_playlist[self.system_playlist_index-1]


    def playNext(self):
        if len(self.user_playlist) == 0 and len(self.system_playlist) == 0:
            return
        if len(self.user_playlist) != 0:
            self.__play(self.user_playlist.pop(0))
            return
        if len(self.user_playlist) != 0:
            self.__play(self.__chooseNext())

    def __play(self,source:CommonSource):
        bs:BaseSource = self.__getPlayableSource(source.getBaseSources())
        if bs == None:
            return
        self.current = source
        self.mpv_player.playByUrl(bs.url, headers=bs.headers)

    def __danmu_add_playlist(self,dmkMsg:DanmakuMessage,*args, **kwargs):
        msg:str = dmkMsg.msg
        if (msg.startswith("点歌")):
            vals = " ".join(msg.split(" ")[1::])
            rs = NeteaseMusicSource.search(vals)
            if rs.isEmpty():
                return
            cm = rs.results[0].source
            cm.load()
            if cm.isValid():
                self.user_playlist.append(cm)
            if self.mpv_player.getProperty(MPVProperty.IDLE):
                self.playNext()

    def __idle_play_next(self,prop,value, *args, **kwargs):
        if value:
            self.current = None
            self.playNext()


print("Initialize global audio bot")
Global_Audio_Bot = AudioBot()

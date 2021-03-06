from typing import List, Type

from audiobot.Playlist import Playlist, PlaylistItem
from config import Config
from liveroom.LiveRoom import LiveRoom
from player.mpv import MPVPlayer, MPVProperty
from plugins.blivedm import DanmakuMessage
from sources.audio import NeteaseMusicSource, BiliAudioSource
from sources.audio.bilibili import BiliAudioListSource
from sources.audio.netease import NeteasePlaylistSource
from sources.base import CommonSource, BaseSource, SourceSelector
from sources.base.interface import WatchableSource
from sources.video.bilibili import BiliVideoSource

from audiobot import MatchEngine


# 祖传代码，难以阅读

class AudioBot():
    selector = SourceSelector(NeteaseMusicSource,
                              BiliAudioSource,
                              BiliVideoSource)

    def __init__(self):
        self.user_playlist = Playlist()
        self.system_playlist = Playlist()
        self.current: PlaylistItem = None
        self.mpv_player: MPVPlayer = None
        self.live_room: LiveRoom = None

    def setPlayer(self, mpv_player: MPVPlayer):
        self.mpv_player = mpv_player
        self.mpv_player.registerPropertyHandler("audiobot.idleplaynext",
                                                MPVProperty.IDLE,
                                                self.__idle_play_next)

    def setLiveRoom(self, live_room: LiveRoom):
        if self.live_room != None:
            self.live_room.clearMsgHandler()
        self.live_room = live_room
        self.live_room.registerMsgHandler("audiobot.msg",
                                          self.__danmu_add_playlist)

    def _loadSystemPlaylist(self, config):
        playlists = config["playlist"]
        songs = config["song"]
        for key, vals in playlists.items():
            if key == "bilibili":
                source_class = BiliAudioListSource
            elif key == "netease":
                source_class = NeteasePlaylistSource
            else:
                continue
            for val in vals:
                c_s = source_class.initFromUrl(val)
                if c_s == None:
                    continue
                c_s.load()
                if not c_s.isValid():
                    return
                for s in c_s.audios:
                    self.system_playlist.append(s)
        for key, vals in songs.items():
            if key == "bilibili":
                source_class = BiliAudioSource
            elif key == "netease":
                source_class = NeteaseMusicSource
            else:
                continue
            for val in vals:
                s = source_class.initFromUrl(val)
                if s == None:
                    continue
                self.system_playlist.append(s)

    def __getPlayableSource(self, sources: dict) -> BaseSource:
        for val in sources.values():
            val: BaseSource
            if isinstance(val, WatchableSource) and isinstance(val, BaseSource):
                return val
        return None

    def playNext(self):
        if len(self.user_playlist) == 0 and len(self.system_playlist) == 0:
            return
        if len(self.user_playlist) != 0:
            self.__play(self.user_playlist.popFirst())
            return
        if len(self.system_playlist) != 0:
            next_item = self.system_playlist.getNext()
            next_item.source.load()
            self.__play(next_item)

    def __play(self, item: PlaylistItem):
        item = MatchEngine.check(item)
        source = item.source
        source.load()
        if not source.isValid():
            return
        bs: BaseSource = self.__getPlayableSource(source.getBaseSources())
        if bs == None:
            self.playNext()
            return
        self.current = item
        self.mpv_player.playByUrl(bs.url, headers=bs.headers)

    def addAudioByUrl(self, url, username="system", source_class: CommonSource.__class__ = None):
        source_class: CommonSource.__class__ = source_class if source_class else self.selector.select(url)
        source, keyword = MatchEngine.search(url, source_class)
        if source == None:
            return
        source.load()
        if source.isValid():
            self.user_playlist.append(source, username=username, keyword=keyword)
        if self.current == None or self.mpv_player.getProperty(MPVProperty.IDLE):
            self.playNext()
            return
        if self.current.username == "system":
            self.playNext()

    def __danmu_add_playlist(self, dmkMsg: DanmakuMessage, *args, **kwargs):
        msg: str = dmkMsg.msg.split(" ")
        if len(msg) < 2:
            return
        hintword, val = msg[0], " ".join(msg[1::])
        if (hintword == "点歌"):
            self.addAudioByUrl(val, username=dmkMsg.uname)
        elif hintword == "点b歌":
            self.addAudioByUrl(val, username=dmkMsg.uname, source_class=BiliAudioSource)
        elif hintword == "点w歌":
            self.addAudioByUrl(val, username=dmkMsg.uname, source_class=NeteaseMusicSource)

    def __idle_play_next(self, prop, value, *args, **kwargs):
        if value:
            self.current = None
            self.playNext()


print("Initialize global audio bot")
Global_Audio_Bot = AudioBot()
Global_Audio_Bot._loadSystemPlaylist(Config.system_playlist)

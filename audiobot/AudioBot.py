import asyncio
from typing import List, Type, Union, Dict

from audiobot.Blacklist import Blacklist
from audiobot.Handler import AudioBotHandlers
from audiobot.Lyric import Lyrics
from audiobot.Playlist import Playlist, PlaylistItem
from audiobot.event import PlaylistAppendEvent
from audiobot.event.audiobot import AudioBotPlayEvent, AudioBotStartEvent
from config import Config
from liveroom.LiveRoom import LiveRoom
from player.mpv import MPVPlayer, MPVProperty
from plugins.blivedm import DanmakuMessage
from sources.audio import NeteaseMusicSource, BiliAudioSource
from sources.audio.bilibili import BiliAudioListSource
from sources.audio.kuwo import KuwoMusicSource
from sources.audio.netease import NeteasePlaylistSource
from sources.base import CommonSource, BaseSource, SourceSelector
from sources.base.interface import WatchableSource
from sources.video.bilibili import BiliVideoSource
from audiobot import MatchEngine
from audiobot import Command

from utils import vasyncio


# 祖传代码，难以阅读

class AudioBot():
    selector = SourceSelector(NeteaseMusicSource,
                              BiliAudioSource,
                              BiliVideoSource,
                              KuwoMusicSource)

    def __init__(self, loop=None):
        self.running = False
        self.user_playlist = Playlist(self,"user_playlist")
        self.system_playlist = Playlist(self,"system_playlist", random_next=True)
        self.history_playlist = Playlist(self, "history_playlist")
        self.blacklist = Blacklist(self)
        self.lyrics = Lyrics(self)
        self.current: PlaylistItem = None
        self.mpv_player: MPVPlayer = None
        self.live_room: LiveRoom = None
        self._loop = asyncio.get_event_loop() if loop == None else loop
        self._command_executors: Dict[str,Command.CommandExecutor] = {}
        self.handlers = AudioBotHandlers()

    def start(self):
        self.running = True
        self.handlers.call(AudioBotStartEvent(self))
        self.__idle_play_next("idle", self.mpv_player.getProperty(MPVProperty.IDLE))

    def setPlayer(self, mpv_player: MPVPlayer):
        self.mpv_player = mpv_player
        self.mpv_player.registerPropertyHandler("audiobot.idleplaynext",
                                                MPVProperty.IDLE,
                                                self.__idle_play_next)
        self.mpv_player.registerPropertyHandler("audiobot.updatelyric",
                                                MPVProperty.TIME_POS,
                                                self.lyrics._raiseEvent)

    def setLiveRoom(self, live_room: LiveRoom):
        if self.live_room != None:
            self.live_room.clearMsgHandler()
        self.live_room = live_room
        self.live_room.registerMsgHandler("audiobot.msg",
                                          self.__process_command)

    def registerCommandExecutor(self, id, cmd: Type[Command.CommandExecutor.__class__]):
        self._command_executors[id] = cmd(self)

    def registerCommandExecutors(self, cmdlist:Dict):
        for id,val in cmdlist.items():
            self.registerCommandExecutor(id,val)

    def _loadSystemPlaylist(self, config):
        try:
            self._thread_call(self.__loadSystemPlaylist,config)
        except:
            pass

    def __loadSystemPlaylist(self, config):
        playlists = config["playlist"]
        songs = config["song"]
        self.system_playlist.random_next = config["random"]
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

        if self.running and self.current is None:
            self.playNext()


    def __getPlayableSource(self, sources: dict) -> BaseSource:
        for val in sources.values():
            val: BaseSource
            if isinstance(val, WatchableSource) and isinstance(val, BaseSource):
                return val

    def playNext(self):
        if len(self.user_playlist) == 0 and len(self.system_playlist) == 0:
            return
        if len(self.user_playlist) != 0:
            self.__thread_play(self.user_playlist.popFirst())
            return
        if len(self.system_playlist) != 0:
            next_item = self.system_playlist.getNext()
            next_item.source.load()
            self.__thread_play(next_item)

    def playByIndex(self, index):
        if index < 0 or index >= len(self.user_playlist):
            return
        self.__thread_play(self.user_playlist.remove(index))

    def addBlacklistByIndex(self, index):
        if index < 0 or index >= len(self.user_playlist):
            return
        self.blacklist.appendPlaylistItem(self.user_playlist.remove(index))

    def play(self, item: PlaylistItem):
        self.__thread_play(item)

    def __thread_play(self, item: PlaylistItem):
        self._thread_call(self.__play,item)

    def __play(self, item: PlaylistItem):
        item.source.load()
        if not item.source.isValid():
            return
        item = MatchEngine.check(item)
        bs: BaseSource = self.__getPlayableSource(item.source.getBaseSources())
        if bs == None:
            if self.current == None:
                self.playNext()
            return
        self.current = item
        self.history_playlist.appendItem(item)
        self.handlers.call(AudioBotPlayEvent(self,item))
        self.lyrics.load(item)
        self.mpv_player.playByUrl(bs.url, headers=bs.headers)

    def addAudioByUrl(self, url, username="system", index=-1,source_class: CommonSource.__class__ = None):
        source_class: CommonSource.__class__ = source_class if source_class else self.selector.select(url)
        source, keyword = MatchEngine.search(url, source_class)
        if source == None:
            return
        source.load()
        if source.isValid():
            if index == -1:
                event:PlaylistAppendEvent = self.user_playlist.append(source, username=username, keyword=keyword)
            else:
                event: PlaylistAppendEvent = self.user_playlist.insert(source, index,username=username, keyword=keyword)
            if event.isCancelled():
                return
            if self.current == None or self.mpv_player.getProperty(MPVProperty.IDLE):
                self.playNext()
                return
            if Config.system_playlist['autoskip'] and self.current.username == "system":
                self.playNext()

    def playAudioByUrl(self, url, username="system",source_class: CommonSource.__class__ = None):
        source_class: CommonSource.__class__ = source_class if source_class else self.selector.select(url)
        source, keyword = MatchEngine.search(url, source_class)
        if source == None:
            return
        source.load()
        if source.isValid():
            event: PlaylistAppendEvent = self.user_playlist.insert(source, 0,username=username, keyword=keyword)
            if event.isCancelled():
                return
            self.playNext()

    def _async_call(self, fun, *args, **kwargs):
        asyncio.ensure_future(vasyncio.asyncwrapper(fun)(*args, **kwargs), loop=self._loop)

    def _thread_call(self,fun, *args, **kwargs):
        self._loop.run_in_executor(None,lambda :fun(*args, **kwargs))

    def __process_command(self, dmkMsg: DanmakuMessage, *args, **kwargs):
        command: str = dmkMsg.msg.split(" ")[0]
        for cmd in self._command_executors.values():
            if cmd.applicable(command):
                cmd.process(command, dmkMsg)

    def __idle_play_next(self, prop, value, *args, **kwargs):
        if value:
            self.current = None
            self.playNext()


print("Initialize global audio bot")
Global_Audio_Bot = AudioBot()
Global_Audio_Bot._loadSystemPlaylist(Config.system_playlist)

from audiobot.Command import Global_Command_Manager
Global_Audio_Bot.registerCommandExecutors(Global_Command_Manager.commands)

# register hooks
from audiobot.hooks import *
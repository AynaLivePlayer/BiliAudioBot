import asyncio
from typing import List, Type, Union, Dict

from audiobot.blacklist import Blacklist
from audiobot.handler import AudioBotHandlers
from audiobot.lyric import Lyrics
from audiobot.playlist import Playlist
from audiobot.audio import AudioItem
from audiobot.event import PlaylistAppendEvent
from audiobot.event.audiobot import AudioBotPlayEvent, AudioBotStartEvent
from audiobot.user import User, PlaylistUser
from config import Config
from liveroom.danmaku import LiveRoom
from liveroom.message import DanmakuMessage
from player.mpv import MPVPlayer, MPVProperty
from sources.audio import NeteaseMusicSource, BiliAudioSource
from sources.audio.bilibili import BiliAudioListSource
from sources.audio.kuwo import KuwoMusicSource
from sources.audio.netease import NeteasePlaylistSource
from sources.base import CommonSource, BaseSource, SourceSelector
from sources.base.interface import WatchableSource
from sources.video.bilibili import BiliVideoSource
from audiobot import MatchEngine
from audiobot import command

from utils import vasyncio


# 祖传代码，难以阅读

class AudioBot():
    selector = SourceSelector(NeteaseMusicSource,
                              BiliAudioSource,
                              BiliVideoSource,
                              KuwoMusicSource)

    def __init__(self, loop=None):
        self.running = False
        self.user_playlist = Playlist(self, "user_playlist")
        self.system_playlist = Playlist(self, "system_playlist", random_next=True)
        self.history_playlist = Playlist(self, "history_playlist")
        self.blacklist = Blacklist(self)
        self.lyrics = Lyrics(self)
        self.current: AudioItem = None
        self.mpv_player: MPVPlayer = None
        self.live_room: LiveRoom = None
        self.loop = asyncio.get_event_loop() if loop == None else loop
        self._command_executors: Dict[str, command.CommandExecutor] = {}
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
            self.live_room.clear_msg_handler()
        self.live_room = live_room
        self.live_room.register_msg_handler("audiobot.msg",
                                          self.__process_command)

    def registerCommandExecutor(self, id, cmd: Type[command.CommandExecutor.__class__]):
        self._command_executors[id] = cmd(self)

    def registerCommandExecutors(self, cmdlist: Dict):
        for id, val in cmdlist.items():
            self.registerCommandExecutor(id, val)

    def _loadSystemPlaylist(self, config):
        try:
            self._thread_call(self.__loadSystemPlaylist, config)
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
                    self.system_playlist.append_raw(s)
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
                self.system_playlist.append_raw(s)

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
            self.__thread_play(self.user_playlist.pop_first())
            return
        if len(self.system_playlist) != 0:
            next_item = self.system_playlist.get_next()
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

    def play(self, item: AudioItem):
        self.__thread_play(item)

    def __thread_play(self, item: AudioItem):
        self._thread_call(self.__play, item)

    def __play(self, item: AudioItem):
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
        self.history_playlist.append(item)
        self.lyrics.load(item)
        self.mpv_player.playByUrl(bs.url, headers=bs.headers)
        self.handlers.call(AudioBotPlayEvent(self, item))

    def addAudioByUrl(self, url, user: User, index=-1, source_class: CommonSource.__class__ = None):
        source_class: CommonSource.__class__ = source_class if source_class else self.selector.select(url)
        source, keyword = MatchEngine.search(url, source_class)
        if source == None:
            return
        source.load()
        if source.isValid():
            if index == -1:
                event: PlaylistAppendEvent = self.user_playlist.append_raw(source, user=user, keyword=keyword)
            else:
                event: PlaylistAppendEvent = self.user_playlist.insert_raw(source, index, user=user, keyword=keyword)
            if event.isCancelled():
                return
            if self.current == None or self.mpv_player.getProperty(MPVProperty.IDLE):
                self.playNext()
                return
            if Config.system_playlist['autoskip'] and self.current.username == PlaylistUser.username:
                self.playNext()

    def playAudioByUrl(self, url, user: User, source_class: CommonSource.__class__ = None):
        source_class: CommonSource.__class__ = source_class if source_class else self.selector.select(url)
        source, keyword = MatchEngine.search(url, source_class)
        if source == None:
            return
        source.load()
        if source.isValid():
            event: PlaylistAppendEvent = self.user_playlist.insert_raw(source, 0, user=user, keyword=keyword)
            if event.isCancelled():
                return
            self.playNext()

    def _async_call(self, fun, *args, **kwargs):
        asyncio.ensure_future(vasyncio.asyncwrapper(fun)(*args, **kwargs), loop=self.loop)

    def _thread_call(self, fun, *args, **kwargs):
        self.loop.run_in_executor(None, lambda: fun(*args, **kwargs))

    def __process_command(self, dmkMsg: DanmakuMessage, *args, **kwargs):
        command: str = dmkMsg.message.split(" ")[0]
        for cmd in self._command_executors.values():
            if cmd.applicable(command):
                cmd.process(command, dmkMsg)

    def __idle_play_next(self, prop, value, *args, **kwargs):
        if value:
            self.current = None
            self.playNext()

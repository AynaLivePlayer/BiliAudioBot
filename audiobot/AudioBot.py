import asyncio
from enum import Enum
from typing import List, Type, Union

from audiobot.Command import DiangeCommand, QiegeCommand
from audiobot.Playlist import Playlist, PlaylistItem
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
from functools import wraps

def asyncwrapper(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        func(*args,**kwargs)
    return wrapper

class AudioBotEvent(Enum):
    PLAY = "play"

    values = [PLAY]

# 祖传代码，难以阅读

class AudioBot():
    selector = SourceSelector(NeteaseMusicSource,
                              BiliAudioSource,
                              BiliVideoSource,
                              KuwoMusicSource)

    def __init__(self,loop=None):
        self.user_playlist = Playlist(self)
        self.system_playlist = Playlist(self,random_next=True)
        self.current: PlaylistItem = None
        self.mpv_player: MPVPlayer = None
        self.live_room: LiveRoom = None
        self._loop = asyncio.get_event_loop() if loop == None else loop
        self._command_executors:List[Command.CommandExecutor] = []
        self._event_handlers = {}

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
                                          self.__process_command)

    def registerCommandExecutor(self,cmd:Type[Command.CommandExecutor.__class__]):
        self._command_executors.append(cmd(self))


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

    def playByIndex(self,index):
        if index<0 or index>=len(self.user_playlist):
            return
        self.__play(self.user_playlist.remove(index))

    def play(self,item:PlaylistItem):
        self.__play(item)

    def __play(self, item: PlaylistItem):
        item.source.load()
        if not item.source.isValid():
            return
        item = MatchEngine.check(item)
        bs: BaseSource = self.__getPlayableSource(item.source.getBaseSources())
        if bs == None:
            if  self.current == None:
                self.playNext()
            return
        self.current = item
        self.__call_handlers(AudioBotEvent.PLAY,item)
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

    def registerEventHanlder(self,event:Union[AudioBotEvent,str],id,func):
        eventkey:str = event.value if isinstance(event,AudioBotEvent) else event
        if self._event_handlers.get(eventkey) == None:
            self._event_handlers[eventkey] = {}
        self._event_handlers[eventkey][id] = func

    def unregisterEventHanlder(self,event:Union[AudioBotEvent,str],id):
        eventkey: str = event.value if isinstance(event,AudioBotEvent) else event
        try:
         self._event_handlers.get(eventkey).pop(id)
        except:
            pass

    def __call_handlers(self,event:Union[AudioBotEvent,str],*args,**kwargs):
        eventkey: str = event.value if isinstance(event,AudioBotEvent) else event
        if self._event_handlers.get(eventkey) == None:
            return
        for func in self._event_handlers.get(eventkey).values():
            self._async_call(func,*args,**kwargs,)

    def _async_call(self,fun,*args,**kwargs):
        asyncio.ensure_future(asyncwrapper(fun)(*args,**kwargs),loop=self._loop)


    def __process_command(self, dmkMsg: DanmakuMessage, *args, **kwargs):
        command: str = dmkMsg.msg.split(" ")[0]
        for cmd in self._command_executors:
            if cmd.applicable(command):
                cmd.process(command,dmkMsg)

    def __idle_play_next(self, prop, value, *args, **kwargs):
        if value:
            self.current = None
            self.playNext()



print("Initialize global audio bot")
Global_Audio_Bot = AudioBot()
Global_Audio_Bot._loadSystemPlaylist(Config.system_playlist)
Global_Audio_Bot.registerCommandExecutor(DiangeCommand)
Global_Audio_Bot.registerCommandExecutor(QiegeCommand)
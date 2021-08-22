from enum import Enum
from typing import List, Union

from audiobot.handler import AudioBotHandlers
from audiobot.playlist import PlaylistItem
from audiobot.event import PlaylistAppendEvent
from audiobot.event.blacklist import BlacklistUpdateEvent, BlacklistLoadedEvent
from config import Config


def _check_song_name(item: PlaylistItem, content, whole):
    content,title = content.lower(),item.source.getTitle().lower()
    if whole:
        return content == title
    else:
        return content in title

def _check_song_id(item: PlaylistItem, content, whole):
    return item.source.getUniqueId() == content

def _check_username(item: PlaylistItem, content, whole):
    un,content = item.username.lower(),content.lower()
    if whole:
        return un == content
    else:
        return content in un


class BlacklistItemType(Enum):
    SONG_NAME = "song_name",False, _check_song_name
    SONG_ID = "song_id",True, _check_song_id
    USERNAME = "username",True,_check_username

    def __init__(self, name, whole_default,func):
        self.identifier = name
        self.check = func
        self.whole_default = whole_default

    @classmethod
    def values(cls) -> List:
        return [member for member in cls]

    @classmethod
    def getByName(cls, name):
        for member in cls:
            if member.name == name or member.identifier == name:
                return member
        return None

class BlacklistItem():
    def __init__(self, bantype: BlacklistItemType, content, whole=None):
        self.bantype: BlacklistItemType = bantype
        self.content = content
        self.whole: bool = bantype.whole_default if whole is None else whole

    def applicable(self, item: PlaylistItem):
        return self.bantype.check(item, self.content, self.whole)

class Blacklist():
    def __init__(self, audio_bot):
        self.audio_bot = audio_bot
        self.blacklist_items: List[BlacklistItem] = []
        self.handlers = AudioBotHandlers()
        self.__register_handlers()
        self.load()

    def remove(self, index):
        if index >= len(self.blacklist_items) or index < 0:
            return
        val = self.blacklist_items.pop(index)
        self.handlers.call(BlacklistUpdateEvent(self))
        return val

    def append(self, bantype:Union[str,BlacklistItemType], content, whole=None):
        if isinstance(bantype,str):
            bantype = BlacklistItemType.getByName(bantype)
        if bantype is None:
            return
        self.appendItem(BlacklistItem(bantype, content, whole = whole))

    def appendItem(self, item: BlacklistItem):
        self.blacklist_items.append(item)
        self.handlers.call(BlacklistUpdateEvent(self))

    def appendPlaylistItem(self, item: PlaylistItem):
        self.append(BlacklistItemType.SONG_NAME,item.source.getTitle())
        self.append(BlacklistItemType.SONG_ID,item.source.getUniqueId())

    def load(self):
        config =Config.blacklist
        for identifier, vals in config.items():
            bantype = BlacklistItemType.getByName(identifier)
            if bantype is None:
                continue
            for val in vals:
                self.blacklist_items.append(BlacklistItem(bantype,
                                                          val["content"],
                                                          whole=val["whole"]))
        self.handlers.call(BlacklistLoadedEvent(self))

    def dump(self):
        retval = dict((member.identifier, []) for member in BlacklistItemType.values())
        for item in self.blacklist_items:
            retval[item.bantype.identifier].append({"content": item.content,
                                                    "whole": item.whole})
        return retval

    def __register_handlers(self):
        self.audio_bot.user_playlist.handlers._register(PlaylistAppendEvent,
                                                        "blacklist.preventblacklistsong",
                                                        self.__check_blacklist)
        self.handlers._register(BlacklistUpdateEvent,
                               "blacklist.writetoconfig",
                               lambda x:self.__write_to_config())

    def __write_to_config(self):
        Config.blacklist = self.dump()

    def __check_blacklist(self, event: PlaylistAppendEvent):
        if event.isCancelled():
            return
        for bl in self.blacklist_items:
            if bl.applicable(event.item):
                event.setCancelled(True)
                return


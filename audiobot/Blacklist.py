from enum import Enum
from typing import List

from audiobot.Handler import AudioBotHandlers
from audiobot.Playlist import PlaylistItem
from audiobot.event import PlaylistAppendEvent

def _check_song_name(item: PlaylistItem, content, whole):
    if whole:
        return content == item.source.getTitle()
    else:
        return content in item.source.getTitle()


class BlacklistItemType(Enum):
    SONG_NAME = "song_name", _check_song_name

    def __init__(self, name, func):
        self.identifier = name
        self.check = func

    @classmethod
    def values(cls) -> List:
        return [member for member in cls]

    @classmethod
    def getByName(cls, name):
        for member in cls:
            if member.name == name or member.identifier == name:
                return name
        return None


class BlackListItem():
    def __init__(self, bantype: BlacklistItemType, content, whole=False):
        self.bantype: BlacklistItemType = bantype
        self.content = content
        self.whole: bool = whole

    def applicable(self, item: PlaylistItem):
        self.bantype.value[1](item, self.content, self.whole)


class Blacklist():
    def __init__(self, audio_bot):
        self.audio_bot = audio_bot
        self.blacklist_items: List[BlackListItem] = []
        self.handlers = AudioBotHandlers()

    def __register_handlers(self):
        self.audio_bot.user_playlist.handlers._register(PlaylistAppendEvent,
                                                        "blacklist.preventblacklistsong",
                                                        self.__check_blacklist)

    def __check_blacklist(self, event: PlaylistAppendEvent):
        if event.isCancelled():
            return
        for bl in self.blacklist_items:
            if bl.applicable(event.item):
                event.setCancelled(True)
                return

    def load(self, config):
        for identifier, vals in config.items():
            bantype = BlacklistItemType.getByName(identifier)
            if bantype is None:
                continue
            for val in vals:
                self.blacklist_items.append(BlackListItem(bantype,
                                                          val["content"],
                                                          whole=val["whole"]))

    def dump(self):
        retval = dict((member.identifier, []) for member in BlacklistItemType.values())
        for item in self.blacklist_items:
            retval[item.bantype.identifier].append({"content": item.content,
                                                    "whole": item.whole})
        return retval

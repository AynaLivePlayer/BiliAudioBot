from typing import Union

from audiobot.user import User
from sources.base import CommonSource
from sources.base.interface import AudioBotInfoSource


class AudioItem():
    def __init__(self, source: Union[CommonSource, AudioBotInfoSource], user: User, keyword):
        self.source = source
        self.user:User =  user
        self.keyword = keyword

    @property
    def username(self):
        return self.user.username
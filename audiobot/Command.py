from typing import Union, List

from plugins.blivedm import DanmakuMessage
from sources.audio import BiliAudioSource, NeteaseMusicSource

class CommandExecutor():
    def __init__(self, audiobot, commands:Union[str, List[str]]):
        self.audiobot = audiobot
        if isinstance(commands,list):
            self.commands = commands
        else:
            self.commands = [commands]

    def applicable(self,command):
        return command in self.commands

    def process(self,command,dmkMsg:DanmakuMessage):
        pass

class DiangeCommand(CommandExecutor):
    def __init__(self,audiobot):
        super().__init__(audiobot,["点歌","点b歌","点w歌","点k歌"])

    def process(self, command,dmkMsg):
        msg: str = dmkMsg.msg.split(" ")
        if len(msg) < 2:
            return
        val = " ".join(msg[1::])
        if (command == "点歌"):
            self.audiobot.addAudioByUrl(val, username=dmkMsg.uname)
        elif command == "点b歌":
            self.audiobot.addAudioByUrl(val, username=dmkMsg.uname, source_class=BiliAudioSource)
        elif command == "点w歌":
            self.audiobot.addAudioByUrl(val, username=dmkMsg.uname, source_class=NeteaseMusicSource)

class QiegeCommand(CommandExecutor):
    def __init__(self,audiobot):
        super().__init__(audiobot,["切歌"])

    def process(self, command,dmkMsg):
        if dmkMsg.uname == self.audiobot.current.username:
            self.audiobot.playNext()
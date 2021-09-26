from typing import List

from audiobot.command import CommandExecutor
from audiobot import Global_Command_Manager
from liveroom.message import DanmakuMessage
from sources.audio import BiliAudioSource, NeteaseMusicSource,KuwoMusicSource

@Global_Command_Manager.register("chaduidiange")
class ChaduiDiangeCommand(CommandExecutor):
    def __init__(self, audiobot):
        super().__init__(audiobot, ["插队点歌", "插队点b歌", "插队点w歌", "插队点k歌"])
        self.cooldowns = {}

    def process(self, command, dmkMsg: DanmakuMessage):
        msg: List[str] = dmkMsg.message.split(" ")
        if len(msg) < 2:
            return
        val = " ".join(msg[1::])
        if not (self.__hasPermission(dmkMsg)):
            return
        if (command == "插队点歌"):
            self.audiobot.addAudioByUrl(val,dmkMsg.user,index=0)
        elif command == "插队点b歌":
            self.audiobot.addAudioByUrl(val,dmkMsg.user,index=0, source_class=BiliAudioSource)
        elif command == "插队点w歌":
            self.audiobot.addAudioByUrl(val,dmkMsg.user,index=0, source_class=NeteaseMusicSource)
        elif command == "插队点k歌":
            self.audiobot.addAudioByUrl(val,dmkMsg.user,index=0, source_class=KuwoMusicSource)

    def __hasPermission(self, dmkMsg: DanmakuMessage):
        try:
            if bool(dmkMsg.admin):
                return True
            if int(dmkMsg.privilege_level) > 0:
                return True
            return False
        except:
            return False
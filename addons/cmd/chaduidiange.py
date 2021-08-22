from audiobot.command import CommandExecutor
from audiobot import Global_Command_Manager
from plugins.blivedm import DanmakuMessage
from sources.audio import BiliAudioSource, NeteaseMusicSource,KuwoMusicSource

@Global_Command_Manager.register("chaduidiange")
class ChaduiDiangeCommand(CommandExecutor):
    def __init__(self, audiobot):
        super().__init__(audiobot, ["插队点歌", "插队点b歌", "插队点w歌", "插队点k歌"])
        self.cooldowns = {}

    def process(self, command, dmkMsg: DanmakuMessage):
        msg: str = dmkMsg.msg.split(" ")
        if len(msg) < 2:
            return
        val = " ".join(msg[1::])
        if not (self.__hasPermission(dmkMsg)):
            return
        if (command == "插队点歌"):
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname)
        elif command == "插队点b歌":
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname, source_class=BiliAudioSource)
        elif command == "插队点w歌":
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname, source_class=NeteaseMusicSource)
        elif command == "插队点k歌":
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname, source_class=KuwoMusicSource)

    def __hasPermission(self, dmkMsg: DanmakuMessage):
        try:
            if bool(dmkMsg.admin):
                return True
            if int(dmkMsg.privilege_type) > 0:
                return True
            return False
        except:
            return False


@Global_Command_Manager.register("forcediange")
class ForceDiangeCommand(CommandExecutor):
    def __init__(self, audiobot):
        super().__init__(audiobot, ["播放", "播放b歌", "播放w歌", "播放k歌"])
        self.cooldowns = {}

    def process(self, command, dmkMsg: DanmakuMessage):
        msg: str = dmkMsg.msg.split(" ")
        if len(msg) < 2:
            return
        val = " ".join(msg[1::])
        if not (self.__hasPermission(dmkMsg)):
            return
        if (command == "播放"):
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname)
        elif command == "播放b歌":
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname, source_class=BiliAudioSource)
        elif command == "播放w歌":
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname, source_class=NeteaseMusicSource)
        elif command == "播放k歌":
            self.audiobot.addAudioByUrl(val,index=0, username=dmkMsg.uname, source_class=KuwoMusicSource)

    def __hasPermission(self, dmkMsg: DanmakuMessage):
        try:
            if bool(dmkMsg.admin):
                return True
            if int(dmkMsg.privilege_type) > 0:
                return True
            return False
        except:
            return False
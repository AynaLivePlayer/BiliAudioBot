from audiobot.Command import CommandExecutor, Global_Command_Manager
from sources.audio import BiliAudioSource, NeteaseMusicSource
from sources.audio.kuwo import KuwoMusicSource

@Global_Command_Manager.register("diange")
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
        elif command == "点k歌":
            self.audiobot.addAudioByUrl(val, username=dmkMsg.uname, source_class=KuwoMusicSource)
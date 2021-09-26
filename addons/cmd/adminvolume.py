from typing import List

from audiobot.command import CommandExecutor
from audiobot import Global_Command_Manager
from liveroom.message import DanmakuMessage

@Global_Command_Manager.register("changevolume")
class ForceDiangeCommand(CommandExecutor):
    def __init__(self, audiobot):
        super().__init__(audiobot, ["调整音量"])
        self.cooldowns = {}


    def process(self, command, dmkMsg: DanmakuMessage):
        msg: List[str] = dmkMsg.message.split(" ")
        if len(msg) < 2:
            return
        val = " ".join(msg[1::])
        if not (self.__hasPermission(dmkMsg)):
            return
        print(val,self.__getpercent(val,self.audiobot.mpv_player.getVolumePercent()))
        if (command == "调整音量"):
            self.audiobot.mpv_player.setVolumePercent(self.__getpercent(val,self.audiobot.mpv_player.getVolumePercent()))

    def __getpercent(self,val,now):
        try:
            val = now+int(val)/100
            if val <=0 or val > 1:
                return now
            return val
        except:
            return now

    def __hasPermission(self, dmkMsg: DanmakuMessage):
        try:
            if bool(dmkMsg.admin):
                return True
            return False
        except:
            return False
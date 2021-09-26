from audiobot.command import CommandExecutor
from audiobot import Global_Command_Manager
from config import Config
from liveroom.message import DanmakuMessage


@Global_Command_Manager.register("qiege")
class QiegeCommand(CommandExecutor):
    def __init__(self,audiobot):
        super().__init__(audiobot,["切歌"])

    def __hasPermission(self, dmkMsg: DanmakuMessage):
        config = Config.commands["qiege"]
        try:
            if config["self"] and (dmkMsg.user.username == self.audiobot.current.username):
                return True
            if config["admin"] and dmkMsg.admin:
                return True
            if config["guard"] and dmkMsg.privilege_level > 0:
                return True
        except:
            return False

    def process(self, command,dmkMsg):
        if self.__hasPermission(dmkMsg):
            self.audiobot.playNext()
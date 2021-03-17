from audiobot.Command import CommandExecutor


class QiegeCommand(CommandExecutor):
    def __init__(self,audiobot):
        super().__init__(audiobot,["切歌"])

    def process(self, command,dmkMsg):
        if dmkMsg.uname == self.audiobot.current.username:
            self.audiobot.playNext()



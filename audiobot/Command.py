from typing import Union, List

from plugins.blivedm import DanmakuMessage


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
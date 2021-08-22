from typing import Union, List, Type

from plugins.blivedm import DanmakuMessage


class CommandExecutor():
    def __init__(self, audiobot, commands: Union[str, List[str]]):
        self.audiobot = audiobot
        if isinstance(commands, list):
            self.commands = commands
        else:
            self.commands = [commands]

    def applicable(self, command):
        return command in self.commands

    def process(self, command, dmkMsg: DanmakuMessage):
        pass


class CommandManager():
    def __init__(self):
        self.commands = {}

    def _register(self, id, command: Type[CommandExecutor]):
        self.commands[id] = command

    def register(self,id):
        def add(fun):
            self._register(id,fun)
            return fun
        return add
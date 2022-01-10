from pyncm import SetCurrentSession, LoadSessionFromString

from audiobot.audiobot import AudioBot
from audiobot.command import CommandManager
from config import Config

pyncmcookie = Config.getCookie("netease", "pyncm")
if pyncmcookie.get("session") is not None:
    try:
        SetCurrentSession(LoadSessionFromString(pyncmcookie.get("session")))
    except:
        pass

print("Initialize global audio bot")
Global_Audio_Bot = AudioBot()
# register hooks
from audiobot.handlers import *

Global_Audio_Bot._loadSystemPlaylist(Config.system_playlist)

Global_Command_Manager = CommandManager()
# register commands
from audiobot.commands import *

Global_Audio_Bot.registerCommandExecutors(Global_Command_Manager.commands)

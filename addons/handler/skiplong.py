from audiobot import Global_Audio_Bot
from audiobot.event import AudioBotPlayEvent
from audiobot.event.audiobot import AudioBotStartEvent
from player.mpv import MPVProperty

max_sec = 300
has_skip = True

def skip_when_time_too_long(property,val,*args):
    global has_skip
    time_pos = 0 if val is None else int(val)
    if time_pos >= max_sec and has_skip:
        has_skip = False
        Global_Audio_Bot.playNext()

def check_play_next(event:AudioBotPlayEvent):
    global has_skip
    has_skip = True

@Global_Audio_Bot.handlers.register(AudioBotStartEvent,"addons.handler.registerskiplong")
def register_skiplong(event:AudioBotStartEvent):
    Global_Audio_Bot.mpv_player.registerPropertyHandler("addon.handler.skip_when_time_too_long",
                                                        MPVProperty.DURATION,
                                                        skip_when_time_too_long)
    Global_Audio_Bot.handlers._register(AudioBotPlayEvent, "addon.handler.skip_when_time_too_long_reset_skip",
                                        check_play_next)

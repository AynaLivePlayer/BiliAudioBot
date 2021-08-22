import asyncio, re
import os
import traceback

import jinja2

from audiobot import Global_Audio_Bot
from audiobot.playlist import PlaylistItem
from audiobot.event import AudioBotPlayEvent
from audiobot.event.lyric import LyricUpdateEvent
from audiobot.event.playlist import PlaylistUpdateEvent
from config import Config
from utils import vfile

DEFAULT_TEMPLATE = "\n".join(["{{current_title[:16:]}} - {{current_artist[:16:]}} - {{current_username[:16:]}}",
                              ""])

TEMPLATE_PLACEHOLDER = {"current_title": str,
                        "current_artist": str,
                        "current_username": str,
                        "current_lyric": str,
                        "playlist_count": int,
                        "playlist": [{
                            "index": int,
                            "title": str,
                            "artist": str,
                            "username": str}]}

TEMPLATE_DEFAULT_VALUES = {"current_title": "",
                           "current_artist": "",
                           "current_username": "",
                           "current_lyric": "",
                           "playlist_count": 0,
                           "playlist": []}


class LocalFileWriterServer():
    def __init__(self, loop=None):
        self._loop = asyncio.get_event_loop() if loop is None else None
        self.template: jinja2.Template = None
        self.content = TEMPLATE_DEFAULT_VALUES.copy()

    # def renderTemplate(self):
    #     output = self.template
    #     for placeholder, key in TEMPLATE_PLACEHOLDER.items():
    #         value = self.content.get(key)
    #         value = "" if value is None else value
    #         placeholder_reg_exp = re.compile(placeholder + "[0-9]*")
    #         number_reg_exp = re.compile("[0-9]+")
    #         for item in placeholder_reg_exp.finditer(self.template):
    #             max_length = number_reg_exp.search(item.group())
    #             max_length = 99999999 if max_length is None else int(max_length.group())
    #             formated_value = ("{:.%d}" % max_length).format(value)
    #             output = placeholder_reg_exp.sub(formated_value, output, count=1)
    #     return output

    def renderTemplate(self):
        try:
            return self.template.render(**self.content)
        except:
            traceback.print_exc()
            return jinja2.Template(DEFAULT_TEMPLATE).render(**self.content)

    async def writeToFile(self):
        self._loop.run_in_executor(None,
                                   lambda: vfile.writeToFile(self.renderTemplate(),
                                                             os.path.dirname(Config.output_channel["file"]["path"]),
                                                             os.path.basename(Config.output_channel["file"]["path"])))

    async def __main_loop(self):
        while True:
            await asyncio.sleep(1)

    def start(self):
        try:
            with open(Config.output_channel["file"]["template"]
                    , "r", encoding="utf-8") as f:
                self.template = jinja2.Template(f.read())
        except:
            self.template = jinja2.Template(DEFAULT_TEMPLATE)
        Global_Audio_Bot.handlers._register(AudioBotPlayEvent.__event_name__,
                                            "localfileserver.updateplaying",
                                            self.__listenAudioBotPlay)

        Global_Audio_Bot.user_playlist.handlers._register(PlaylistUpdateEvent.__event_name__,
                                                          "localfileserver.updateplaylist",
                                                          self.__listenPlaylistUpdate)

        Global_Audio_Bot.lyrics.handlers._register(LyricUpdateEvent,
                                                   "localfileserver.updatelyric",
                                                   self.__listenLyricUpdate)

        return self.__main_loop()

    def __listenAudioBotPlay(self, event: AudioBotPlayEvent):
        item: PlaylistItem = event.item
        if item == None:
            self.content.update({"current_title": "",
                                 "current_artist": "",
                                 "current_username": ""})
        else:
            self.content.update({"current_title": item.source.getTitle(),
                                 "current_artist": item.source.getArtist(),
                                 "current_username": item.username})
        asyncio.ensure_future(self.writeToFile(), loop=self._loop)

    def __listenPlaylistUpdate(self, event: PlaylistUpdateEvent):
        playlist = event.playlist.playlist
        self.content.update({"playlist_count": str(len(playlist))})
        playlist_data = []
        for index, item in enumerate(playlist):
            item: PlaylistItem
            playlist_data.append({"index": index,
                                  "title": item.source.getTitle(),
                                  "artist": item.source.getArtist(),
                                  "username": item.username})
        self.content["playlist"] = playlist_data
        asyncio.ensure_future(self.writeToFile(), loop=self._loop)

    def __listenLyricUpdate(self, event: LyricUpdateEvent):
        self.content.update({"current_lyric": event.lyric.lyric})
        asyncio.ensure_future(self.writeToFile(), loop=self._loop)

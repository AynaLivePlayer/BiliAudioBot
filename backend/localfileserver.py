import asyncio, re
import os

from audiobot.AudioBot import Global_Audio_Bot
from audiobot.Playlist import PlaylistItem
from audiobot.event import AudioBotPlayEvent
from audiobot.event.playlist import PlaylistUpdateEvent
from config import Config
from utils import vfile

DEFAULT_TEMPLATE = "\n".join(["=current_title=16 - =current_artist=16 - =current_username=16",])

TEMPLATE_PLACEHOLDER = {"=current_title=": "current_title",
                        "=current_artist=": "current_artist",
                        "=current_username=": "current_artist",
                        # "=playlist_index=": "playlist_index",
                        # "=playlist_title=": "playlist_title",
                        # "=playlist_artist=": "playlist_artist",
                        # "=playlist_username=": "playlist_username"
                        }


class LocalFileWriterServer():
    def __init__(self, loop=None):
        self._loop = asyncio.get_event_loop() if loop is None else None
        self.template = ""
        self.content = dict()

    def renderTemplate(self):
        output = self.template
        for placeholder, key in TEMPLATE_PLACEHOLDER.items():
            value = self.content.get(key)
            value = "" if value is None else value
            placeholder_reg_exp = re.compile(placeholder + "[0-9]*")
            number_reg_exp = re.compile("[0-9]+")
            for item in placeholder_reg_exp.finditer(self.template):
                max_length = number_reg_exp.search(item.group())
                max_length = 99999999 if max_length is None else int(max_length.group())
                formated_value = ("{:.%d}" % max_length).format(value)
                output = placeholder_reg_exp.sub(formated_value, output, count=1)
        return output

    async def writeToFile(self):
        self._loop.run_in_executor(None,
                                   lambda :vfile.writeToFile(self.renderTemplate(),
                                                             os.path.dirname(Config.output_channel["file"]["path"]),
                                                             os.path.basename(Config.output_channel["file"]["path"])))

    async def __main_loop(self):
        while True:
            await asyncio.sleep(1)

    def start(self):
        try:
            with open(Config.output_channel["file"]["template"]
                    ,"r",encoding="utf-8") as f:
                self.template = f.read()
        except:
            self.template = DEFAULT_TEMPLATE
        Global_Audio_Bot.registerEventHanlder(AudioBotPlayEvent.__event_name__,
                                              "localfileserver.updateplaying",
                                              self.__listenAudioBotPlay)

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
        asyncio.ensure_future(self.writeToFile(),loop=self._loop)

    # def __listenPlaylistUpdate(self, event: PlaylistUpdateEvent):
    #     playlist = event.playlist.playlist
    #     playlist_data = []
    #     for item in playlist:
    #         item: PlaylistItem
    #         playlist_data.append({"playlist_title": item.source.getTitle(),
    #                               "playlist_artist": item.source.getArtist(),
    #                               "playlist_username": item.username})
    #     return playlist_data

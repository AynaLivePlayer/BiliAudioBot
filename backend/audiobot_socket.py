import asyncio

from audiobot.AudioBot import Global_Audio_Bot
from audiobot.Playlist import PlaylistItem
from audiobot.event import AudioBotPlayEvent
from audiobot.event.lyric import LyricUpdateEvent
from audiobot.event.playlist import PlaylistUpdateEvent

loop = asyncio.get_event_loop()
websockets = []


def sendJsonData(data):
    for ws in websockets:
        asyncio.ensure_future(ws.send_json(data), loop=loop)


@Global_Audio_Bot.user_playlist.handlers.register(PlaylistUpdateEvent.__event_name__,
                                                  "websocket.updateplaylist")
def listenPlaylistUpdate(event: PlaylistUpdateEvent):
    sendJsonData({event.__event_name__: parsePlaylistUpdate(event.playlist.playlist)})


def parsePlaylistUpdate(playlist):
    playlist_data = []
    for item in playlist:
        item: PlaylistItem
        cover_url = item.source.getCover().url if item.source.getCover() != None else None
        playlist_data.append({"title": item.source.getTitle(),
                              "artist": item.source.getArtist(),
                              "cover": cover_url,
                              "username": item.username})
    return playlist_data


@Global_Audio_Bot.handlers.register(AudioBotPlayEvent.__event_name__,
                                    "websocket.updateplaying")
def listenAudioBotPlay(event: AudioBotPlayEvent):
    item: PlaylistItem = event.item
    sendJsonData({event.__event_name__: parseAudioBotPlayData(item)})


def parseAudioBotPlayData(item: PlaylistItem):
    if item == None:
        return {"title": "",
                "artist": "",
                "cover": "",
                "username": ""}
    cover_url = item.source.getCover().url if item.source.getCover() != None else None
    return {"title": item.source.getTitle(),
            "artist": item.source.getArtist(),
            "cover": cover_url,
            "username": item.username}

@Global_Audio_Bot.handlers.register(LyricUpdateEvent,
                                       "websocket.updatelyric")
def listenLyricUpdate(event: LyricUpdateEvent):
    sendJsonData({event.__event_name__: {"lyric":event.lyric.lyric}})


async def sendInitialData(ws):
    await ws.send_json({PlaylistUpdateEvent.__event_name__:
                            parsePlaylistUpdate(Global_Audio_Bot.user_playlist.playlist)})
    await ws.send_json({AudioBotPlayEvent.__event_name__:
                            parseAudioBotPlayData(Global_Audio_Bot.current)})

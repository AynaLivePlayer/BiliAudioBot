import asyncio
import traceback

from audiobot import Global_Audio_Bot
from audiobot.playlist import PlaylistItem
from audiobot.event import AudioBotPlayEvent
from audiobot.event.lyric import LyricUpdateEvent
from audiobot.event.playlist import PlaylistUpdateEvent
from backend.aioserver import app
loop = asyncio.get_event_loop()
websockets = []


def getImgRedirectedUrl(url):
    try:
        return str(app.router["autoredirect"].url_for().with_query({"url": url}))
    except:
        traceback.print_exc()
        return ""

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
        cover_url = item.source.getCover().url if item.source.getCover() != None else ""
        playlist_data.append({"title": item.source.getTitle(),
                              "artist": item.source.getArtist(),
                              "cover": getImgRedirectedUrl(cover_url),
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
    cover_url = item.source.getCover().url if item.source.getCover() != None else ""
    return {"title": item.source.getTitle(),
            "artist": item.source.getArtist(),
            "cover": getImgRedirectedUrl(cover_url),
            "username": item.username}


@Global_Audio_Bot.lyrics.handlers.register(LyricUpdateEvent,
                                    "websocket.updatelyric")
def listenLyricUpdate(event: LyricUpdateEvent):
    sendJsonData({event.__event_name__: {"lyric": event.lyric.lyric}})


async def sendInitialData(ws):
    await ws.send_json({PlaylistUpdateEvent.__event_name__:
                            parsePlaylistUpdate(Global_Audio_Bot.user_playlist.playlist)})
    await ws.send_json({AudioBotPlayEvent.__event_name__:
                            parseAudioBotPlayData(Global_Audio_Bot.current)})

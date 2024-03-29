from typing import List, Type

from audiobot.handler import AudioBotHandlers
from audiobot.audio import AudioItem
from audiobot.event.audiobot import FindSearchResultEvent
from sources.audio import BiliAudioSource, NeteaseMusicSource
from sources.audio.kuwo import KuwoMusicSource
from sources.base import CommonSource
from sources.base.interface import SearchableSource

SEARCH_ENGINE_LIST:List[SearchableSource.__class__] = [BiliAudioSource,KuwoMusicSource,NeteaseMusicSource]
DEFAULT_SEARCH_ENGINE = NeteaseMusicSource

HANDLERS = AudioBotHandlers()

def check(item:AudioItem):
    source = item.source
    if source == None:
        return item
    if isinstance(source,NeteaseMusicSource):
        item.source = matchNetease(source,keyword=item.keyword)
        return item
    return item

def search(url, source_class:CommonSource.__class__):
    if source_class == None:
        source_class = DEFAULT_SEARCH_ENGINE
    source = source_class.initFromUrl(url)
    if source == None:
        if issubclass(source_class,SearchableSource):
            return searchFirst(url, engine=source_class), url
        else:
            return searchFirst(url), url
    else:
        return source,""

def searchFirst(url, engine:SearchableSource.__class__=None):
    engine = engine if engine else DEFAULT_SEARCH_ENGINE
    search_results = engine.search(url)
    if search_results == None or search_results.isEmpty():
        return None
    for result in search_results.results:
        event = FindSearchResultEvent(result)
        HANDLERS.call(event)
        if event.isCancelled():
            continue
        return result.source
    return search_results.results[0].source

def matchNetease(netease:NeteaseMusicSource,keyword=""):
    if not netease.vip and netease.available:
        return netease
    else:
        for engine in SEARCH_ENGINE_LIST:
            if keyword != "":
                result = searchFirst(keyword, engine=engine)
                if result != None:
                    netease.getBaseSources = result.getBaseSources
                    netease.getSourceName = result.getSourceName
                    # result.getTitle = netease.getTitle
                    # result.getArtist = netease.getArtist
                    # result.getCover = netease.getCover
                    return netease
            result = searchFirst(" ".join([netease.title] + netease.artists), engine=engine)
            if result != None:
                netease.getBaseSources = result.getBaseSources
                netease.getSourceName = result.getSourceName
                # result.getTitle = netease.getTitle
                # result.getArtist = netease.getArtist
                # result.getCover = netease.getCover
                return netease
    return netease

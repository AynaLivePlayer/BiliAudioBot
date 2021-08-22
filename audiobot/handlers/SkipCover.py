import re

from audiobot.event.audiobot import FindSearchResultEvent
from sources.base import SearchResult
from sources.base.interface import AudioBotInfoSource

coverlist = [r"\(.*cover.*\)",
             r"\(.*翻唱.*\)",
             r"\(.*翻自.*\)",
             r"\(.*remix.*\)",
             r"（.*cover.*）",
             r"（.*翻唱.*\）",
             r"（.*翻自.*\）",
             r"\（.*remix.*\）",
             ]


def skip_cover(event: FindSearchResultEvent):
    if event.isCancelled():
        return
    result: SearchResult = event.search_result
    if not isinstance(result.source, AudioBotInfoSource):
        return
    for pattern in coverlist:
        if re.search(pattern, result.source.getTitle()) is not None:
            event.setCancelled(True)
            return

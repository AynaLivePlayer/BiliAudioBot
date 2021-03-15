from audiobot.event.base import BaseAudioBotEvent, CancellableEvent


class PlaylistAppendEvent(BaseAudioBotEvent,
                          CancellableEvent):
    __event_name__ = "playlist_append"

    def __init__(self, playlist, item):
        self.playlist = playlist
        self.item = item
        self.cancel = False

    def isCancelled(self):
        return self.cancel

    def setCancelled(self, b):
        self.cancel = b


class PlaylistUpdateEvent(BaseAudioBotEvent):
    __event_name__ = "playlist_update"

    def __init__(self, playlist):
        self.playlist = playlist

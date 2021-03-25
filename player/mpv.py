from enum import Enum

from plugins import mpv_lib

class MPVEvent(Enum):
    FILE_START = "START_FILE"
    FILE_LOADED = "FILE_LOADED"
    FILE_END = "END_FILE"

class MPVProperty(Enum):
    VOLUME = "volume"
    PAUSE = "pause"
    IDLE = "idle-active"

    TIME_POS = "time-pos"
    PERCENT_POS = "percent-pos"
    DURATION = "duration"

class MPVPlayer:
    MAX_VOLUME = 120

    def __init__(self,window_id:str):
        self.window_id = window_id
        self.mpv_core = mpv_lib.MPV(wid=self.window_id)
        self.property_handlers = {}
        self.event_handlers = {}

    def isPaused(self):
        return self.mpv_core._get_property("pause")

    def isPlaying(self):
        return not self.isPaused()

    def isLoaded(self):
        return not self.mpv_core._get_property("idle-active")

    def play(self):
        self.mpv_core._set_property("pause", False)

    def pause(self):
        self.mpv_core._set_property("pause", True)

    def toggle(self):
        self.mpv_core._set_property("pause",not self.isPaused())

    def goto(self,time):
        self.mpv_core.seek(time,reference="absolute")

    def stop(self):
        self.mpv_core.stop()

    def getVolume(self):
        return self.mpv_core._get_property("volume")

    def getVolumePercent(self):
        return self.mpv_core._get_property("volume") / self.MAX_VOLUME

    def setVolume(self,volume):
        self.mpv_core._set_property("volume", volume)

    def setVolumePercent(self,percent):
        self.mpv_core._set_property("volume", self.MAX_VOLUME * percent)

    def playByUrl(self, url, **options):
        if options.get("headers") != None:
            headers = options.pop("headers")
            if headers.get("user-agent") != None:
                self.mpv_core._set_property("user-agent", headers.get("user-agent"))
            if headers.get("referer") != None:
                self.mpv_core._set_property("referrer", headers.get("referer"))
            self.mpv_core._set_property("http-header-fields",
                                          self.__parseHeader(headers))
        self.mpv_core.play(url)
        self.play()

    def __parseHeader(self,header):
        headerlist = []
        for key,val in header.items():
            if key == "referer":
                headerlist.append("referrer:{}".format(val))
                continue
            headerlist.append("{}:{}".format(key,val))
        return headerlist

    def setProperty(self,property:MPVProperty,val):
        self.mpv_core._set_property(property.value,val)

    def getProperty(self,property:MPVProperty):
        return self.mpv_core._get_property(property.value)

    def registerPropertyHandler(self,id,property:MPVProperty,func):
        self.unregisterPropertyHandler(id)
        self.property_handlers[id] = (property.value,func)
        self.mpv_core.observe_property(property.value,func)

    def unregisterPropertyHandler(self,id):
        currrent = self.property_handlers.get(id)
        if currrent != None:
            self.mpv_core.unobserve_property(currrent[0],currrent[1])
            self.property_handlers.pop(id)

    def clearPropertyHandler(self):
        for key in self.property_handlers.keys():
            self.unregisterPropertyHandler(key)

    def registerEventHandler(self,id,property:MPVEvent,func):
        self.unregisterEventHandler(id)
        self.event_handlers[id] = self.mpv_core.event_callback(property.value)(func)

    def unregisterEventHandler(self,id):
        currrent = self.event_handlers.get(id)
        if currrent != None:
            self.mpv_core.unregister_event_callback(currrent)
            self.event_handlers.pop(id)

    def clearEventHandler(self):
        self.mpv_core._event_callbacks.clear()
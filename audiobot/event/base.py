class BaseAudioBotEvent():
    __event_name__ = "base"

class CancellableEvent():

    def isCancelled(self):
        return False

    def setCancelled(self,b):
        pass

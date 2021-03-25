from typing import Type, Union

from audiobot.event.base import BaseAudioBotEvent

class AudioBotHandlers():
    def __init__(self):
        self._event_handlers = {}

    def _register(self, event:Union[str,Type[BaseAudioBotEvent]], id, func):
        event_name = event if isinstance(event,str) else event.__event_name__
        if self._event_handlers.get(event_name) is None:
            self._event_handlers[event_name] = {}
        self._event_handlers[event_name][id] = func

    def register(self,event:Union[str,Type[BaseAudioBotEvent]],id):
        def add(func):
            self._register(event,id,func)
            return func
        return add

    def unregister(self,event_name,id):
        try:
            self._event_handlers.get(event_name).pop(id)
        except:
            pass

    def call(self, event: BaseAudioBotEvent):
        event_name: str = event.__event_name__
        if self._event_handlers.get(event_name) is None:
            return
        for func in self._event_handlers.get(event_name).values():
            func(event)
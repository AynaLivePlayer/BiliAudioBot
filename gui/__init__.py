import asyncio
from functools import wraps

from mttkinter import mtTkinter as tk
from tkinter import ttk, PhotoImage
from tkinter import Menu
from tkinter.ttk import Notebook

from gui.PlaylistGUI import PlaylistGUI
from gui.MPVGUI import MPVGUI
from gui.RoomGUI import RoomGUI
from gui.SearchGUI import SearchGUI

def asyncwrapper(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        func(*args,**kwargs)
    return wrapper


class MainWindow():
    def __init__(self, loop=None, interval=1 / 20):
        self.window = tk.Tk()
        self.interval = interval
        self.window.title("重生之我是欧菲手")
        self.tab_controller: Notebook = ttk.Notebook(self.window)
        self.menu_controller = Menu(self.window)
        self._loop = asyncio.get_event_loop() if loop == None else loop
        self._initialize()

    def _initialize(self):
        self.window.iconphoto(True,PhotoImage(file='resource/favicon.png'))
        self.window.resizable(False, False)
        self.window.geometry("720x480")
        self.tab_controller.pack(expand=1, fill="both")

    def getTabController(self) -> Notebook:
        return self.tab_controller

    def async_update(self, func, *args, **kwargs):
        asyncio.ensure_future(asyncwrapper(func)(*args, **kwargs), loop=self._loop)

    async def _update(self):
        while True:
            try:
                self.window.update()
                await asyncio.sleep(self.interval)
            except:
                break

    def start(self):
        self.createWidgets()
        return self._update()

    def createWidgets(self):
        mpv = MPVGUI(self)
        room = RoomGUI(self)
        playlist = PlaylistGUI(self)
        search = SearchGUI(self)
        room.createWidgets()
        playlist.createWidgets()
        search.createWidgets()
        mpv.createWidgets()

        mpv.initialize()
        room.initialize()
        playlist.initialize()
        search.initialize()

from tkinter import ttk, scrolledtext
from audiobot import Global_Audio_Bot
from liveroom import Global_Room_Manager
import tkinter as tk
import gui
from config import Config
from utils.vtranslation import getTranslatedText as _

class RoomGUI():
    def __init__(self,main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.room_id = tk.StringVar()
        self.output_label = tk.StringVar()

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("AudioBot"))

        self.room_id.set(Config.default_room)

    def createWidgets(self):

        frame_main = ttk.LabelFrame(self.widget, text="AudioBot Test")
        frame_main.grid(column=0, row=0, padx=8, pady=4)

        # ========== input frame ================

        frame_input = ttk.Frame(frame_main)
        frame_input.grid(column=0, row=0, padx=8, pady=4,sticky=tk.W)

        # Creating check box for commands
        ttk.Label(frame_input, text=_("enter room id:")) \
            .grid(column=0, row=0, sticky=tk.W, padx=8, pady=4)

        room_id_input = ttk.Entry(frame_input,
                                     width=16,
                                     textvariable=self.room_id)
        room_id_input.grid(column=1, row=0, padx=8, pady=4)

        play_button = ttk.Button(frame_input, width=8, text=_("connect"), command=self.__confirmroom)
        play_button.grid(column=2, row=0)

        # ========== output frame ================

        frame_output = ttk.Frame(frame_main)
        frame_output.grid(column=0, row=1, padx=8, pady=4, sticky=tk.W)

        # Creating check box for commands
        output_label = ttk.Label(frame_output,
                                 width = 64,
                                 textvariable = self.output_label)
        output_label.grid(column=0, row=0, sticky=tk.W, padx=8, pady=4)

    def __confirmroom(self):
        self.output_label.set("connect")
        self._startRoom()

    def _startRoom(self):
        Global_Room_Manager.stop_all()
        lr = Global_Room_Manager.add_live_room(self.room_id.get())
        Config.default_room = self.room_id.get()
        Global_Room_Manager.start_room(self.room_id.get())
        Global_Audio_Bot.setLiveRoom(lr)
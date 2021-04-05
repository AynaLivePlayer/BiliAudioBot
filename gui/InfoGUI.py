from tkinter import ttk
import tkinter as tk
import gui
from audiobot.AudioBot import Global_Audio_Bot
from audiobot.event.audiobot import FindSearchResultEvent
from audiobot.hooks import SkipCover
from config import Config
from audiobot import MatchEngine
from gui.MPVGUI import MPVGUI
from gui.factory import ConfigGUIFactory, TextEntry
from player.mpv import MPVPlayer, MPVProperty
from utils.vtranslation import getTranslatedText as _

class InfoGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("EtcInfo"))

    def createWidgets(self):
        frame_obsinfo = ttk.LabelFrame(self.widget, text=_("OBS output"))
        frame_obsinfo.pack(fill=tk.BOTH, expand="yes", padx=4)
        frame_appinfo = ttk.LabelFrame(self.widget, text=_("Application Information"))
        frame_appinfo.pack(fill=tk.BOTH, expand="yes", padx=4)

        # ============== obs info =========================

        frame_obsinfo_1 = ttk.Frame(frame_obsinfo)
        frame_obsinfo_1.grid(column=0,row=0,sticky=tk.W,padx=8,pady=8)

        frame_obsinfo_2 = ttk.Frame(frame_obsinfo)
        frame_obsinfo_2.grid(column=0, row=1,sticky=tk.W,padx=8,pady=8)

        frame_obsinfo_3 = ttk.Frame(frame_obsinfo)
        frame_obsinfo_3.grid(column=0, row=2,sticky=tk.W,padx=8,pady=8)

        frame_obsinfo_4 = ttk.Frame(frame_obsinfo)
        frame_obsinfo_4.grid(column=0, row=3,sticky=tk.W,padx=8,pady=8)

        frame_obsinfo_5 = ttk.Frame(frame_obsinfo)
        frame_obsinfo_5.grid(column=0, row=4, sticky=tk.W, padx=8, pady=8)

        ttk.Label(frame_obsinfo_1,text = _("Current Song Info:")).pack(side=tk.LEFT,padx=4)
        TextEntry.getTextEntry(frame_obsinfo_1,
                               "http://127.0.0.1:{}/currentplaying"
                               .format(Config.output_channel["web"]["port"]),
                               width = 32).pack(side=tk.LEFT,padx=4)
        ttk.Label(frame_obsinfo_1, text=_("CSS:")).pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_obsinfo_1,
                               ".playing-info {}",
                               width=16).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_obsinfo_2, text=_("Current Song Lyric:")).pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_obsinfo_2,
                               "http://127.0.0.1:{}/currentlyric"
                               .format(Config.output_channel["web"]["port"]),
                               width=32).pack(side=tk.LEFT, padx=4)
        ttk.Label(frame_obsinfo_2, text=_("CSS:")).pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_obsinfo_2,
                               ".playing-lyric {}",
                               width=16).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_obsinfo_3, text=_("Current Song Cover:")).pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_obsinfo_3,
                               "http://127.0.0.1:{}/currentcover"
                               .format(Config.output_channel["web"]["port"]),
                               width=32).pack(side=tk.LEFT, padx=4)
        ttk.Label(frame_obsinfo_3, text=_("CSS:")).pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_obsinfo_3,
                               ".playing-cover {}",
                               width=16).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_obsinfo_4, text=_("TextInfo:")).pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_obsinfo_4,
                               "http://127.0.0.1:{}/textinfo"
                               .format(Config.output_channel["web"]["port"]),
                               width=32).pack(side=tk.LEFT, padx=4)

        # ============== application info =========================

        frame_appinfo_1 = ttk.Frame(frame_appinfo)
        frame_appinfo_1.grid(column=0, row=0, sticky=tk.W, padx=8, pady=8)

        frame_appinfo_2 = ttk.Frame(frame_appinfo)
        frame_appinfo_2.grid(column=0, row=1, sticky=tk.W, padx=8, pady=8)

        frame_appinfo_3 = ttk.Frame(frame_appinfo)
        frame_appinfo_3.grid(column=0, row=2, sticky=tk.W, padx=8, pady=8)

        frame_appinfo_4 = ttk.Frame(frame_appinfo)
        frame_appinfo_4.grid(column=0, row=3, sticky=tk.W, padx=8, pady=8)

        frame_appinfo_5 = ttk.Frame(frame_appinfo)
        frame_appinfo_5.grid(column=0, row=4, sticky=tk.W, padx=8, pady=8)

        frame_appinfo_6 = ttk.Frame(frame_appinfo)
        frame_appinfo_6.grid(column=0, row=5, sticky=tk.W, padx=8, pady=8)

        ttk.Label(frame_appinfo_1, text=_("Author:")).pack(side=tk.LEFT, padx=4)
        ttk.Label(frame_appinfo_1, text="Aynakeya && Nearl_Official").pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_appinfo_2, text="Github:").pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_appinfo_2,
                               "https://github.com/LXG-Shadow/BiliAudioBot",
                               width=64).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_appinfo_3, text="Aynakeya Bilibili:").pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_appinfo_3,
                               "https://space.bilibili.com/10003632",
                               width=64).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_appinfo_4, text="Nearl_Official Bilibili:").pack(side=tk.LEFT, padx=4)
        TextEntry.getTextEntry(frame_appinfo_4,
                               "https://space.bilibili.com/5953957",
                               width=64).pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_appinfo_5, text=_("Thanks to:")).pack(side=tk.LEFT, padx=4)
        ttk.Label(frame_appinfo_5, text="greats3an/pyncm, xfgryujk/blivedm, jaseg/python-mpv").pack(side=tk.LEFT, padx=4)

        ttk.Label(frame_appinfo_6, text=_("Version:")).pack(side=tk.LEFT, padx=4)
        ttk.Label(frame_appinfo_6, text=Config.version).pack(side=tk.LEFT, padx=4)
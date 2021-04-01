from tkinter import ttk
import tkinter as tk

from audiobot.AudioBot import Global_Audio_Bot
from gui.factory.PlayerProgressBar import PlayerProgressBar
from player.mpv import MPVPlayer, MPVProperty
import gui


class MPVGUI():
    MAX_VOLUME = 128
    instance = None

    @staticmethod
    def getInstance():
        return MPVGUI.instance

    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())

        # self.volume = tk.DoubleVar()
        self.progress = tk.IntVar()
        self.mpv_player: MPVPlayer = None
        self.mpv_window_id = ""

    @property
    def progressPercent(self):
        return self.progress.get() / 100

    def initialize(self):
        MPVGUI.instance = self
        self.mpv_player = MPVPlayer(self.mpv_window_id)
        self.mpv_player.registerPropertyHandler("mpvgui.syncprogress",
                                                MPVProperty.PERCENT_POS,
                                                self._syncProgress)
        Global_Audio_Bot.setPlayer(self.mpv_player)
        self._pause()


    def createWidgets(self):
        self.main_window.getTabController().add(self.widget, text="MPV")

        frame_main = ttk.LabelFrame(self.widget,
                                    text="MPV Player")
        frame_main.grid_columnconfigure(0, weight=1)
        frame_main.grid_columnconfigure(2, weight=1)
        frame_main.pack(fill="both", expand="yes", padx=8, pady=4)

        # ==== Row 0 ====

        frame_row_1 = ttk.Frame(frame_main)
        frame_row_1.grid(column=1, row=0, padx=8, pady=4)

        frame_player = ttk.Frame(frame_row_1,
                                 width=510, height=340)
        frame_player.grid(column=0, row=0, sticky="news")

        self.mpv_window_id = str(int(frame_player.winfo_id()))

        # ==== Row 2 ====
        frame_row_2 = ttk.Frame(frame_main)
        frame_row_2.grid(column=1, row=1, padx=8, pady=4)

        # add progress scale
        progress_scale = PlayerProgressBar(frame_row_2,
                                 orient=tk.HORIZONTAL,
                                 variable=self.progress,
                                 from_=0,
                                 to=100,
                                 length = 510,
                                 command = self._setProgress)
        progress_scale.grid(column=0, row=0)

        # ==== Row 3 ====

        frame_row_3 = ttk.Frame(frame_main)
        frame_row_3.grid(column=1, row=2, padx=8, pady=4)

        # Adding pause Button
        pause_button = ttk.Button(frame_row_3, width=8, text="pause", command=self._pause)
        pause_button.grid(column=2, row=0)

        # Adding play Button
        play_button = ttk.Button(frame_row_3, width=8, text="play", command=self._play)
        play_button.grid(column=1, row=0)

        # Adding stop Button
        stop_button = ttk.Button(frame_row_3, width=8, text="stop", command=self._stop)
        stop_button.grid(column=0, row=0)

    def _parseHeader(self,header):
        headerlist = []
        for key,val in header.items():
            if key == "referer":
                headerlist.append("referrer:{}".format(val))
                continue
            headerlist.append("{}:{}".format(key,val))
        return headerlist

    def _play(self):
        self.mpv_player.play()
        self._syncProgress()

    def _pause(self):
        self.mpv_player.pause()

    def _stop(self):
        self.mpv_player.stop()

    def _syncProgress(self,*args):
        if self.mpv_player.getProperty(MPVProperty.PERCENT_POS) == None:
            self.progress.set(0)
        self.progress.set(self.mpv_player.getProperty(MPVProperty.PERCENT_POS))

    def _setProgress(self,*args):
        tmp = self.mpv_player.getVolume()
        self.mpv_player.setVolume(0)
        if self.mpv_player.getProperty(MPVProperty.PERCENT_POS) == None:
            self.progress.set(0)
            return
        self.mpv_player.setProperty(MPVProperty.PERCENT_POS, self.progress.get())
        self.mpv_player.setVolume(tmp)
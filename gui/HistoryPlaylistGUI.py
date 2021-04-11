from tkinter import ttk
from audiobot.AudioBot import Global_Audio_Bot
import tkinter as tk
import gui
from audiobot.event.playlist import PlaylistUpdateEvent
from gui.factory.ToolTip import ToolTip
from utils.vtranslation import getTranslatedText as _


class HistoryPlaylistGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.audio_bot = Global_Audio_Bot
        self.playlist_tree: ttk.Treeview = None

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("Play History"))

        self.audio_bot.history_playlist.handlers._register("playlist_update",
                                                     "playhistory.update",
                                                     self.__updateTree)


    def createWidgets(self):
        frame_main = ttk.LabelFrame(self.widget, text="Play History")
        frame_main.pack(fill="both", expand="yes", padx=8, pady=4)

        frame_playlist = ttk.Frame(frame_main)
        frame_playlist.pack(fill=tk.X, expand="yes", side=tk.TOP)

        frame_playing = ttk.Frame(frame_main)
        frame_playing.pack(fill=tk.X, expand="yes", side=tk.BOTTOM)

        # ========== playlist frame ================
        frame_display = ttk.Frame(frame_playlist)
        frame_display.grid(column=0, row=0, padx=4, pady=4)
        frame_move = ttk.Frame(frame_playlist)
        frame_move.grid(column=1, row=0, padx=4, pady=4)

        self.playlist_tree = ttk.Treeview(frame_display, height=16, selectmode="browse")
        self.playlist_tree["columns"] = ("title", "artist", "source", "user")
        self.playlist_tree.column("#0", width=32, minwidth=32)
        self.playlist_tree.column("title", width=256, minwidth=256)
        self.playlist_tree.column("artist", width=128, minwidth=128)
        self.playlist_tree.column("source", width=128, minwidth=128)
        self.playlist_tree.column("user", width=64+32, minwidth=64+32)

        self.playlist_tree.heading("#0", text="#", anchor=tk.W)
        self.playlist_tree.heading("title", text=_("title"), anchor=tk.W)
        self.playlist_tree.heading("artist", text=_("artist"), anchor=tk.W)
        self.playlist_tree.heading("source", text=_("source"), anchor=tk.W)
        self.playlist_tree.heading("user", text=_("user"), anchor=tk.W)

        self.playlist_tree.grid(column=0, row=0)
        self.playlist_tree.bind('<Button-1>', self.__disableTreeSeperator)

        self.playlist_tree.bind('<ButtonRelease-1>', self.__clearFocusIfEmpty)

        playlist_add_button = ttk.Button(frame_move, width=3, text="+",
                                          command=self.__addCurrent)
        playlist_add_button.grid(column=0, row=0, pady=2)

        ToolTip(playlist_add_button, _("add to the playlist"))

        playlist_play_button = ttk.Button(frame_move, width=3, text="▶",
                                          command = self.__playCurrent)
        playlist_play_button.grid(column=0, row=1, pady=2)

        ToolTip(playlist_play_button, _("play selected"))

        playlist_clear_button = ttk.Button(frame_move, width=3, text="∅",
                                               command=self.audio_bot.history_playlist.clear)
        playlist_clear_button.grid(column=0, row=2, pady=2)

        ToolTip(playlist_clear_button, _("clear the list"))

        playlist_bl_button = ttk.Button(frame_move, width=3, text="⛒",
                                          command=self.__addCurrentToBlacklist)
        playlist_bl_button.grid(column=0, row=3, pady=2)

        ToolTip(playlist_bl_button, _("add to blacklist"))

    def __playCurrent(self):
        index = self.__getTreeviewFocusIndex()
        if index == -1:
            return
        item = self.audio_bot.history_playlist.get(index)
        self.audio_bot.play(item)

    def __addCurrent(self):
        index = self.__getTreeviewFocusIndex()
        if index == -1:
            return
        item = self.audio_bot.history_playlist.get(index)
        self.audio_bot.user_playlist.appendItem(item)

    def __addCurrentToBlacklist(self):
        index = self.__getTreeviewFocusIndex()
        if index == -1:
            return
        item = self.audio_bot.history_playlist.get(index)
        self.audio_bot.blacklist.appendPlaylistItem(item)

    def __disableTreeSeperator(self, event):
        if self.playlist_tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def __getTreeviewFocusIndex(self):
        id = self.playlist_tree.item(self.playlist_tree.focus())["text"]
        return -1 if id  == "" else int(id)

    def __clearFocusIfEmpty(self,event):
        if self.playlist_tree.identify_region(event.x, event.y) == "nothing":
            self.__clearTreeviewFocus()

    def __clearTreeviewFocus(self):
        self.playlist_tree.focus('')
        for item in self.playlist_tree.selection():
            self.playlist_tree.selection_remove(item)

    def __updateTree(self, event:PlaylistUpdateEvent):
        playlist = event.playlist
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        for index, item in enumerate(playlist.playlist):
            source = item.source
            self.playlist_tree.insert("", index, text=index, values=(source.getTitle(),
                                                                     source.getArtist(),
                                                                     source.getSourceName(),
                                                                     item.username))
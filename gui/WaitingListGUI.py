from tkinter import ttk
from audiobot.AudioBot import Global_Audio_Bot
import tkinter as tk
import gui
from audiobot.event.playlist import PlaylistUpdateEvent
from utils.vtranslation import getTranslatedText as _


class WaitingListGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.audio_bot = Global_Audio_Bot
        self.playlist_tree: ttk.Treeview = None

    def initialize(self):
        self.audio_bot.system_playlist.handlers._register("playlist_update",
                                                     "playlist.update",
                                                     self.__updateTree)

    def createWidgets(self):
        self.main_window.getTabController().add(self.widget, text=_("System Playlist"))

        frame_main = ttk.LabelFrame(self.widget, text="Playlist demo")
        frame_main.pack(fill="both", expand="yes", padx=8, pady=4)

        frame_playlist = ttk.Frame(frame_main)
        frame_playlist.pack(fill=tk.X, expand="yes", side=tk.TOP)

        frame_playing = ttk.Frame(frame_main)
        frame_playing.pack(fill=tk.X, expand="yes", side=tk.BOTTOM)

        # ========== playlist frame ================
        frame_display = ttk.Frame(frame_playlist)
        frame_display.grid(column=0, row=0, padx=4, pady=4)
        frame_scroll = ttk.Frame(frame_playlist)
        frame_scroll.grid(column=1, row=0, padx=4, pady=4)

        self.playlist_tree = ttk.Treeview(frame_display, height="13", selectmode="browse")
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

        verscrlbar = ttk.Scrollbar(frame_scroll,
                                   orient="vertical",
                                   command=self.playlist_tree.yview)

        self.playlist_tree.configure(xscrollcommand = verscrlbar.set)
        verscrlbar.grid(column=0, row=0)

        # playlist_play_button = ttk.Button(frame_move, width=3, text="▶",
        #                                   command = lambda :self.audio_bot.playByIndex(self.__getTreeviewFocusIndex()))
        # playlist_play_button.grid(column=0, row=5, pady=2)
        #
        # ToolTip(playlist_play_button, _("play selected"))

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

    def __move(self,index,target_index):
        self.audio_bot.user_playlist.move(index, target_index)

    def __updateTree(self, event:PlaylistUpdateEvent):
        user_playlist = event.playlist
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        for index, item in enumerate(user_playlist.playlist):
            source = item.source
            self.playlist_tree.insert("", index, text=index, values=(source.getTitle(),
                                                                     source.getArtist(),
                                                                     source.getSourceName(),
                                                                     item.username))
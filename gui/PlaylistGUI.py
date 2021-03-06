from tkinter import ttk, scrolledtext
from audiobot.AudioBot import Global_Audio_Bot
import tkinter as tk
import gui


class PlaylistGUI():
    def __init__(self,main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.playlist_tree:ttk.Treeview = None

    def initialize(self):
        Global_Audio_Bot.user_playlist.registerHandler("playlist.update",
                                                       self.__updateTree)

    def createWidgets(self):
        self.main_window.getTabController().add(self.widget, text="Playlist")

        frame_main = ttk.LabelFrame(self.widget, text="Playlist test")
        frame_main.grid(column=0, row=0, padx=8, pady=4)

        # ========== display frame ================

        frame_display = ttk.Frame(frame_main)
        frame_display.grid(column=0, row=0, padx=8, pady=4,sticky=tk.W)

        self.playlist_tree = ttk.Treeview(frame_display,selectmode="browse")
        self.playlist_tree["columns"] = ("title", "artist", "source","user")
        self.playlist_tree.column("#0", width=64, minwidth=16, stretch=tk.NO)
        self.playlist_tree.column("title", width=256, minwidth=16, stretch=tk.NO)
        self.playlist_tree.column("artist", width=128, minwidth=16,stretch=tk.NO)
        self.playlist_tree.column("source", width=128, minwidth=16, stretch=tk.NO)
        self.playlist_tree.column("user", width=128, minwidth=16, stretch=tk.NO)

        self.playlist_tree.heading("#0", text="index", anchor=tk.W)
        self.playlist_tree.heading("title", text="title", anchor=tk.W)
        self.playlist_tree.heading("artist", text="artist", anchor=tk.W)
        self.playlist_tree.heading("source", text="source", anchor=tk.W)
        self.playlist_tree.heading("user", text="user", anchor=tk.W)

        self.playlist_tree.grid(column=0, row=0)



    def __updateTree(self,user_playlist):
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        for index,item in enumerate(user_playlist.playlist):
            source = item.source
            self.playlist_tree.insert("",index,text = index,values  = (source.getTitle(),
                                                                       source.getArtist(),
                                                                       source.getSourceName(),
                                                                       item.username))
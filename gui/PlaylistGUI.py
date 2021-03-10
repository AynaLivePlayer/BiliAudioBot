from tkinter import ttk
from audiobot.AudioBot import Global_Audio_Bot
import tkinter as tk
import gui
from audiobot.Playlist import PlaylistItem
from sources.base import PictureSource
from utils import vhttp, vwrappers
from PIL import Image, ImageTk
import io


class PlaylistGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.audio_bot = Global_Audio_Bot
        self.playlist_tree: ttk.Treeview = None
        self.playing_cover: ttk.Label = None
        self.playing_title: tk.StringVar = tk.StringVar()
        self.playing_source: tk.StringVar = tk.StringVar()
        self.empty_image = ImageTk.PhotoImage(Image.new("RGB",(100,100),(255,255,255)))

    def initialize(self):
        self.audio_bot.user_playlist.registerHandler("playlist.update",
                                                     self.__updateTree)

        self.audio_bot.registerEventHanlder("play", "playinginfo.update",
                                            self.__updatePlayingInfo)

    def createWidgets(self):
        self.main_window.getTabController().add(self.widget, text="Playlist")

        frame_main = ttk.LabelFrame(self.widget, text="Playlist demo")
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

        self.playlist_tree = ttk.Treeview(frame_display, height="13", selectmode="browse")
        self.playlist_tree["columns"] = ("title", "artist", "source", "user")
        self.playlist_tree.column("#0", width=32, minwidth=32)
        self.playlist_tree.column("title", width=256, minwidth=256)
        self.playlist_tree.column("artist", width=128, minwidth=128)
        self.playlist_tree.column("source", width=128, minwidth=128)
        self.playlist_tree.column("user", width=64+32, minwidth=64+32)

        self.playlist_tree.heading("#0", text="#", anchor=tk.W)
        self.playlist_tree.heading("title", text="title", anchor=tk.W)
        self.playlist_tree.heading("artist", text="artist", anchor=tk.W)
        self.playlist_tree.heading("source", text="source", anchor=tk.W)
        self.playlist_tree.heading("user", text="user", anchor=tk.W)

        self.playlist_tree.grid(column=0, row=0)
        self.playlist_tree.bind('<Button-1>', self.__disableTreeSeperator)

        self.playlist_tree.bind('<ButtonRelease-1>', self.__clearFocusIfEmpty)

        playlist_superup_button = ttk.Button(frame_move, width=3, text="⭡",
                                             command = lambda :self.__move(self.__getTreeviewFocusIndex(),0))
        playlist_superup_button.grid(column=0, row=0, pady=2)

        playlist_up_button = ttk.Button(frame_move, width=3, text="⏶",
                                        command = lambda :self.__move(self.__getTreeviewFocusIndex(),self.__getTreeviewFocusIndex()-1))
        playlist_up_button.grid(column=0, row=1, pady=2)

        playlist_down_button = ttk.Button(frame_move, width=3, text="⏷",
                                  command = lambda :self.__move(self.__getTreeviewFocusIndex(),self.__getTreeviewFocusIndex()+1))
        playlist_down_button.grid(column=0, row=2, pady=2)

        playlist_superdown_button = ttk.Button(frame_move, width=3, text="⭣",
                                       command = lambda :self.__move(self.__getTreeviewFocusIndex(),99999))
        playlist_superdown_button.grid(column=0, row=3, pady=2)

        playlist_delete_button = ttk.Button(frame_move, width=3, text="X",
                                    command = lambda :self.audio_bot.user_playlist.remove(self.__getTreeviewFocusIndex()))
        playlist_delete_button.grid(column=0, row=4, pady=2)

        playlist_play_button = ttk.Button(frame_move, width=3, text="▶",
                                          command = lambda :self.audio_bot.playByIndex(self.__getTreeviewFocusIndex()))
        playlist_play_button.grid(column=0, row=5, pady=2)

        # ========== Playing frame ================
        frame_cover = ttk.Frame(frame_playing)
        frame_cover.grid(column=0, row=0, padx=4)
        frame_playinfo = ttk.Frame(frame_playing)
        frame_playinfo.grid(column=1, row=0, padx=4)
        frame_playinfo_0 = ttk.Frame(frame_playinfo)
        frame_playinfo_0.grid(column=0, row=0, padx=4, sticky=tk.W)
        frame_playinfo_1 = ttk.Frame(frame_playinfo)
        frame_playinfo_1.grid(column=0, row=1, padx=4, sticky=tk.W)
        frame_playinfo_2 = ttk.Frame(frame_playinfo)
        frame_playinfo_2.grid(column=0, row=2, padx=4, sticky=tk.W)

        self.playing_cover = ttk.Label(frame_cover, width=100)
        self.playing_cover.grid(column=0, row=0)

        playing_source = ttk.Label(frame_playinfo_0, textvariable=self.playing_source)
        playing_source.grid(column=0, row=0, pady=2, padx=2)

        playing_title_label = ttk.Label(frame_playinfo_1, textvariable=self.playing_title)
        playing_title_label.grid(column=0, row=0, pady=2, padx=2)

        playing_previous_button = ttk.Button(frame_playinfo_2, width=3, text="⏮",
                                             command=lambda: self.audio_bot.mpv_player.goto(0))
        playing_previous_button.grid(column=0, row=0, pady=2, padx=2)

        playing_pause_button = ttk.Button(frame_playinfo_2, width=3, text="⏯",
                                          command=lambda: self.audio_bot.mpv_player.toggle())
        playing_pause_button.grid(column=1, row=0, pady=2, padx=2)

        playing_next_button = ttk.Button(frame_playinfo_2, width=3, text="⏭", command=self.audio_bot.playNext)
        playing_next_button.grid(column=2, row=0, pady=2, padx=2)

    @vwrappers.TryExceptRetNone
    def __loadCover(self, ps: PictureSource):
        if ps == None:
            print("123")
            self.playing_cover.configure(image=self.empty_image)
            self.playing_cover.image = self.empty_image
            return
        data = vhttp.httpGet(ps.url, headers=ps.headers).content
        img = ImageTk.PhotoImage(Image.open(io.BytesIO(data)).resize((100, 100)))
        self.playing_cover.configure(image=img)
        self.playing_cover.image = img

    def __updatePlayingInfo(self, item: PlaylistItem):
        self.playing_source.set("Source: {}".format(item.source.getSourceName()))
        self.playing_title.set(("{title:.24} - - - " +
                                "{artist:.16} - - - " +
                                "({user:.16})").format(title=item.source.getTitle(),
                                                                artist=item.source.getArtist(),
                                                                user=item.username))
        self.__loadCover(item.source.getCover())


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

    def __updateTree(self, user_playlist):
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        for index, item in enumerate(user_playlist.playlist):
            source = item.source
            self.playlist_tree.insert("", index, text=index, values=(source.getTitle(),
                                                                     source.getArtist(),
                                                                     source.getSourceName(),
                                                                     item.username))
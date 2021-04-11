from tkinter import ttk
from audiobot.AudioBot import Global_Audio_Bot
import tkinter as tk
import gui
from audiobot.event import AudioBotPlayEvent
from audiobot.event.playlist import PlaylistUpdateEvent
from config import Config
from gui.factory.PlayerProgressBar import PlayerProgressBar
from gui.factory.ToolTip import ToolTip
from player.mpv import MPVProperty
from sources.base import PictureSource
from utils import vhttp, vwrappers
from PIL import Image, ImageTk
from utils.vtranslation import getTranslatedText as _
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
        self.time_pos = 0
        self.duration = 0
        self.playing_time: tk.StringVar = tk.StringVar()
        self.empty_image = ImageTk.PhotoImage(Image.new("RGB",(100,100),(255,255,255)))

        self.progress = tk.DoubleVar()
        self.volume = tk.DoubleVar()

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("Playlist"))

        self.audio_bot.user_playlist.handlers._register("playlist_update",
                                                     "playlist.update",
                                                     self.__updateTree)

        self.audio_bot.handlers._register("audiobot_play",
                                            "playinginfo.update",
                                            self.__updatePlayingInfo)

        self.audio_bot.mpv_player.registerPropertyHandler("playinginfo.syncprogress",
                                                MPVProperty.PERCENT_POS,
                                                self.__syncProgress)

        self.audio_bot.mpv_player.registerPropertyHandler("playinginfo.watchtime",
                                                          MPVProperty.TIME_POS,
                                                          self.__syncTime)

        self.audio_bot.mpv_player.registerPropertyHandler("playinginfo.watchduration",
                                                          MPVProperty.DURATION,
                                                          self.__syncTime)

        self.audio_bot.mpv_player.registerPropertyHandler("playinginfo.watchvolume",
                                                          MPVProperty.VOLUME,
                                                          self.__syncVolume)

        if Config.player_volume > 1 :
            Config.player_volume = 1
        self.volume.set(Config.player_volume*100)
        self.audio_bot.mpv_player.setVolumePercent(Config.player_volume)


    def createWidgets(self):

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
        self.playlist_tree.heading("title", text=_("title"), anchor=tk.W)
        self.playlist_tree.heading("artist", text=_("artist"), anchor=tk.W)
        self.playlist_tree.heading("source", text=_("source"), anchor=tk.W)
        self.playlist_tree.heading("user", text=_("user"), anchor=tk.W)

        self.playlist_tree.grid(column=0, row=0)
        self.playlist_tree.bind('<Button-1>', self.__disableTreeSeperator)

        self.playlist_tree.bind('<ButtonRelease-1>', self.__clearFocusIfEmpty)

        playlist_superup_button = ttk.Button(frame_move, width=3, text="⭡",
                                             command = lambda :self.__move(self.__getTreeviewFocusIndex(),0))
        playlist_superup_button.grid(column=0, row=0, pady=2)

        ToolTip(playlist_superup_button, _("move to top"))

        playlist_up_button = ttk.Button(frame_move, width=3, text="⏶",
                                        command = lambda :self.__move(self.__getTreeviewFocusIndex(),self.__getTreeviewFocusIndex()-1))
        playlist_up_button.grid(column=0, row=1, pady=2)

        ToolTip(playlist_up_button, _("move up"))

        playlist_down_button = ttk.Button(frame_move, width=3, text="⏷",
                                  command = lambda :self.__move(self.__getTreeviewFocusIndex(),self.__getTreeviewFocusIndex()+1))
        playlist_down_button.grid(column=0, row=2, pady=2)

        ToolTip(playlist_down_button, _("move down"))

        playlist_superdown_button = ttk.Button(frame_move, width=3, text="⭣",
                                       command = lambda :self.__move(self.__getTreeviewFocusIndex(),99999))
        playlist_superdown_button.grid(column=0, row=3, pady=2)

        ToolTip(playlist_superdown_button, _("move to bottom"))

        playlist_delete_button = ttk.Button(frame_move, width=3, text="X",
                                    command = lambda :self.audio_bot.user_playlist.remove(self.__getTreeviewFocusIndex()))
        playlist_delete_button.grid(column=0, row=4, pady=2)

        ToolTip(playlist_delete_button, _("delete song from list"))

        playlist_clear_button = ttk.Button(frame_move, width=3, text="∅",
                                           command=self.audio_bot.user_playlist.clear)
        playlist_clear_button.grid(column=0, row=5, pady=2)

        ToolTip(playlist_clear_button, _("clear the list"))

        playlist_play_button = ttk.Button(frame_move, width=3, text="▶",
                                          command = lambda :self.audio_bot.playByIndex(self.__getTreeviewFocusIndex()))
        playlist_play_button.grid(column=0, row=6, pady=2)

        ToolTip(playlist_play_button, _("play selected"))

        playlist_bl_button = ttk.Button(frame_move, width=3, text="⛒",
                                          command=lambda: self.audio_bot.addBlacklistByIndex(self.__getTreeviewFocusIndex()))
        playlist_bl_button.grid(column=0, row=7, pady=2)

        ToolTip(playlist_bl_button, _("add to blacklist"))

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
        frame_playinfo_3 = ttk.Frame(frame_playinfo)
        frame_playinfo_3.grid(column=0, row=3, padx=4, sticky=tk.W)

        self.playing_cover = ttk.Label(frame_cover, width=100)
        self.playing_cover.grid(column=0, row=0)

        self.playing_cover.configure(image=self.empty_image)
        self.playing_cover.image = self.empty_image

        playing_source = ttk.Label(frame_playinfo_0, textvariable=self.playing_source)
        playing_source.grid(column=0, row=0, pady=2, padx=2)
        self.playing_source.set("Waiting")

        playing_title_label = ttk.Label(frame_playinfo_1, textvariable=self.playing_title)
        playing_title_label.grid(column=0, row=0, pady=2, padx=2)
        self.playing_title.set("Waiting")

        playing_previous_button = ttk.Button(frame_playinfo_2, width=3, text="⏮",
                                             command=lambda: self.audio_bot.mpv_player.goto(0))
        playing_previous_button.grid(column=0, row=0, pady=2, padx=2)

        ToolTip(playing_previous_button,_("replay"))

        playing_pause_button = ttk.Button(frame_playinfo_2, width=3, text="⏯",
                                          command=lambda: self.audio_bot.mpv_player.toggle())
        playing_pause_button.grid(column=1, row=0, pady=2, padx=2)

        ToolTip(playing_pause_button, _("play/pause"))

        playing_next_button = ttk.Button(frame_playinfo_2, width=3, text="⏭", command=self.audio_bot.playNext)
        playing_next_button.grid(column=2, row=0, pady=2, padx=2)

        ToolTip(playing_next_button, _("play next"))

        ttk.Label(frame_playinfo_2,text= "       ").grid(column=3, row=0)

        # add volume scale
        ttk.Label(frame_playinfo_2, text=_("Volume: ")) \
            .grid(column=4, row=0)
        volume_scale = PlayerProgressBar(frame_playinfo_2,
                                         orient=tk.HORIZONTAL,
                                         variable=self.volume,
                                         from_=0,
                                         to=100,
                                         length = 64+32,
                                         command = self.__setVolume)
        volume_scale.grid(column=5, row=0)

        # add progress scale
        progress_scale = PlayerProgressBar(frame_playinfo_3,
                                           orient=tk.HORIZONTAL,
                                           variable=self.progress,
                                           from_=0,
                                           to=100,
                                           length=512-32,
                                           command = self.__setProgress)
        progress_scale.grid(column=0, row=0)

        time_label = ttk.Label(frame_playinfo_3,textvariable=self.playing_time)
        time_label.grid(column=1, row=0,padx=4)


    @vwrappers.TryExceptRetNone
    def __loadCover(self, ps: PictureSource):
        if ps == None:
            self.playing_cover.configure(image=self.empty_image)
            self.playing_cover.image = self.empty_image
            return
        data = vhttp.httpGet(ps.url, headers=ps.headers).content
        img = ImageTk.PhotoImage(Image.open(io.BytesIO(data)).resize((100, 100)))
        self.playing_cover.configure(image=img)
        self.playing_cover.image = img

    def __updatePlayingInfo(self, event: AudioBotPlayEvent):
        item = event.item
        self.playing_source.set(_("Source: {}").format(item.source.getSourceName()))
        self.playing_title.set(("{title:.24} - - - " +
                                "{artist:.16} - - - " +
                                "({user:.16})").format(title=item.source.getTitle(),
                                                                artist=item.source.getArtist(),
                                                                user=item.username))
        self.main_window.threading_update(self.__loadCover,item.source.getCover())



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

    def __setProgress(self,val,*args):
        if self.audio_bot.mpv_player.getProperty(MPVProperty.PERCENT_POS) == None:
            self.progress.set(0)
            return
        self.audio_bot.mpv_player.setProperty(MPVProperty.PERCENT_POS, float(val))


    def __syncProgress(self,property,val,*args):
        if val == None:
            self.progress.set(0)
            return
        self.progress.set(val)

    def __syncTime(self,property,val,*args):
        if property == "time-pos":
            self.time_pos = 0 if val is None else int(val)
        elif property == "duration":
            self.duration = 0 if val is None else int(val)
        self.playing_time.set("{}/{}".format(self.__formatTime(self.time_pos),
                                             self.__formatTime(self.duration)))
    def __formatTime(self,stime):
        minutes = stime // 60
        seconds = stime % 60
        return "{:d}:{:0>2d}".format(minutes,seconds)

    def __setVolume(self,val,*args):
        Config.player_volume = float(val)/100
        self.audio_bot.mpv_player.setVolumePercent(float(val)/100)

    def __syncVolume(self,property,val,*args):
        self.volume.set(self.audio_bot.mpv_player.getVolumePercent()*100)
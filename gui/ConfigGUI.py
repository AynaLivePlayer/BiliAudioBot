from tkinter import ttk
import tkinter as tk
import gui
from audiobot.AudioBot import Global_Audio_Bot
from audiobot.event.audiobot import FindSearchResultEvent
from audiobot.hooks import SkipCover
from config import Config
from audiobot import MatchEngine
from gui.MPVGUI import MPVGUI
from gui.factory import ConfigGUIFactory
from player.mpv import MPVPlayer, MPVProperty
from utils.vtranslation import getTranslatedText as _

class ConfigGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("DG Config"))

    def createWidgets(self):
        frame_diange = ttk.LabelFrame(self.widget, text=_("DG Config"))
        frame_diange.pack(fill=tk.X, expand="yes", padx=4)

        frame_qiege = ttk.LabelFrame(self.widget, text=_("QG Config"))
        frame_qiege.pack(fill=tk.X, expand="yes", padx=4)

        frame_playlist = ttk.LabelFrame(self.widget, text=_("Playlist Config"))
        frame_playlist.pack(fill=tk.X, expand="yes", padx=4)

        frame_audio_device = ttk.LabelFrame(self.widget, text=_("Audio Device"))
        frame_audio_device.pack(fill=tk.X, expand="yes", padx=4)

        frame_etc = ttk.LabelFrame(self.widget, text=_("Experimental Feature"))
        frame_etc.pack(fill=tk.X, expand="yes", padx=4)

        # ========== frame_diange ================
        frame_diange_1 = ttk.Frame(frame_diange)
        frame_diange_1.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)
        frame_diange_2 = ttk.Frame(frame_diange)
        frame_diange_2.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)

        ttk.Label(frame_diange_1, text=_("DG Permission: ")).grid(column=0, row=0)

        # visitor perm
        ConfigGUIFactory.getCheckButton(frame_diange_1, _("Visitor"),
                                        Config.commands["diange"], "visitor",
                                        bool, int).grid(column=1, row=0, padx=8)

        # guard perm
        ConfigGUIFactory.getCheckButton(frame_diange_1, _("Guard"),
                                        Config.commands["diange"], "guard",
                                        bool, int).grid(column=2, row=0, padx=8)

        # admin perm
        ConfigGUIFactory.getCheckButton(frame_diange_1, _("Admin"),
                                        Config.commands["diange"], "admin",
                                        bool, int).grid(column=3, row=0, padx=8)

        ttk.Label(frame_diange_2, text=_("DG Cooldown (s): ")).grid(column=0, row=0)
        ConfigGUIFactory.getInput(frame_diange_2, Config.commands["diange"], "cooldown",
                                  ConfigGUIFactory.ConvertWithDefault(int, 0),
                                  str).grid(column=1, row=0, padx=8)
        ttk.Label(frame_diange_2, text=_("DG Max number: ")).grid(column=2, row=0)
        ConfigGUIFactory.getInput(frame_diange_2, Config.commands["diange"], "limit",
                                  ConfigGUIFactory.ConvertWithDefault(int, 128),
                                  str).grid(column=3, row=0, padx=8)

        # ========== frame_qiege ================
        frame_qiege_1 = ttk.Frame(frame_qiege)
        frame_qiege_1.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)

        # self perm
        ConfigGUIFactory.getCheckButton(frame_qiege_1, _("Self"),
                                        Config.commands["qiege"], "self",
                                        bool, int).grid(column=1, row=0, padx=8)

        # guard perm
        ConfigGUIFactory.getCheckButton(frame_qiege_1, _("Guard"),
                                        Config.commands["qiege"], "guard",
                                        bool, int).grid(column=2, row=0, padx=8)

        # admin perm
        ConfigGUIFactory.getCheckButton(frame_qiege_1, _("Admin"),
                                        Config.commands["qiege"], "admin",
                                        bool, int).grid(column=3, row=0, padx=8)

        # ========== frame_playlist ================
        frame_playlist_1 = ttk.Frame(frame_playlist)
        frame_playlist_1.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)
        frame_playlist_2 = ttk.Frame(frame_playlist)
        frame_playlist_2.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)
        frame_playlist_3 = ttk.Frame(frame_playlist)
        frame_playlist_3.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)

        ttk.Label(frame_playlist_1, text=_("Enter netease playlist id (separate by ,) (restart after modified )")).grid(
            column=0, row=0)
        ttk.Label(frame_playlist_1, text="      ").grid(column=1, row=0)
        ttk.Label(frame_playlist_1, text=_("Example: 1234565,1234564")).grid(column=2, row=0)
        input1, button1 = ConfigGUIFactory.getInputWithButton(frame_playlist_2,
                                                              Config.system_playlist["playlist"],
                                                              "netease",
                                                              ConfigGUIFactory.ConvertWithDefault(
                                                                  lambda x: list(map(lambda x: str(int(x)),
                                                                                     x.split(","))), []),
                                                              lambda x: ",".join(x),
                                                              input_kwargs={"width": 64},
                                                              button_kwargs={"text": _("Update Playlist")})
        input1.grid(column=0, row=0, padx=8)
        button1.grid(column=1, row=0, padx=8)

        ConfigGUIFactory.getCheckButton(frame_playlist_3, _("Random System Playlist"),
                                        Config.system_playlist, "random",
                                        bool, int).grid(column=0, row=0, padx=8)
        ConfigGUIFactory.getCheckButton(frame_playlist_3, _("Skip when user add a song"),
                                        Config.system_playlist, "autoskip",
                                        bool, int).grid(column=1, row=0, padx=8)

        # ========== frame audio_device ================

        frame_audio_device_1 = ttk.Frame(frame_audio_device)
        frame_audio_device_1.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)

        player: MPVPlayer = Global_Audio_Bot.mpv_player
        ad_info = player.getProperty(MPVProperty.AUDIO_DEVICE_LIST)
        ad_vals = [d["description"] for d in ad_info]
        ad_dn_map = dict((d["description"], d["name"]) for d in ad_info)
        ad_nd_map = dict((d["name"], d["description"]) for d in ad_info)

        def get_set_audio_device(audio_bot, ad_map, name):
            ad_desc = ad_map[name]
            p: MPVPlayer = audio_bot.mpv_player
            p.setProperty(MPVProperty.AUDIO_DEVICE, name)
            return ad_desc
        audio_device_selection = ConfigGUIFactory.getBoxSelector(frame_audio_device_1,
                                                                 Config.audio_device,
                                                                 "id",
                                                                 ad_vals,
                                                                 ConfigGUIFactory.ConvertWithDefault(
                                                                     lambda x: ad_dn_map[x], "auto"),
                                                                 ConfigGUIFactory.ConvertWithDefault(
                                                                     lambda x: get_set_audio_device(Global_Audio_Bot,
                                                                                                      ad_nd_map,
                                                                                                      x),
                                                                     "Autoselect device"),
                                                                 state='readonly',
                                                                 width=32)
        ttk.Label(frame_audio_device_1, text=_("Select audio device: ")).grid(column=0, row=0)
        audio_device_selection.grid(column=1, row=0,padx=8)

        # ========== frame exp ================
        variable = tk.IntVar()

        def tst():
            if variable.get() == 0:
                MatchEngine.HANDLERS.unregister(FindSearchResultEvent, "filtercover")
            else:
                MatchEngine.HANDLERS._register(FindSearchResultEvent, "filtercover",
                                               SkipCover.skip_cover)

        check_button = tk.Checkbutton(frame_etc,
                                      text=_("filter cover"),
                                      variable=variable,
                                      command=tst)
        check_button.grid(column=0, row=0)

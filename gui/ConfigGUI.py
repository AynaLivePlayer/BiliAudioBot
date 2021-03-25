from tkinter import ttk, scrolledtext
import tkinter as tk
import gui
from audiobot.event.audiobot import FindSearchResultEvent
from audiobot.hooks import SkipCover
from config import Config
from audiobot import MatchEngine
from gui.factory import ConfigGUIFactory
from utils.vtranslation import getTranslatedText as _

class ConfigGUI():
    def __init__(self,main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())

    def initialize(self):
        pass

    def createWidgets(self):
        self.main_window.getTabController().add(self.widget, text=_("DG Config"))

        frame_diange = ttk.LabelFrame(self.widget, text=_("DG Config"))
        frame_diange.pack(fill=tk.X, expand="yes", padx=4)

        frame_qiege = ttk.LabelFrame(self.widget, text=_("QG Config"))
        frame_qiege.pack(fill=tk.X, expand="yes", padx=4)

        frame_etc = ttk.LabelFrame(self.widget, text=_("Experimental Feature"))
        frame_etc.pack(fill=tk.X, expand="yes", padx=4)


        # ========== frame_diange ================
        frame_diange_1 = ttk.Frame(frame_diange)
        frame_diange_1.pack(fill=tk.X, side = tk.TOP,expand="yes", padx=2, pady=2)
        frame_diange_2 = ttk.Frame(frame_diange)
        frame_diange_2.pack(fill=tk.X, side=tk.TOP, expand="yes", padx=2, pady=2)

        ttk.Label(frame_diange_1, text=_("DG Permission: ")).grid(column=0, row=0)

        # visitor perm
        ConfigGUIFactory.getCheckButton(frame_diange_1,_("Visitor"),
                                        Config.commands["diange"],"visitor",
                                        bool,int).grid(column=1, row=0,padx=8)

        # guard perm
        ConfigGUIFactory.getCheckButton(frame_diange_1, _("Guard"),
                                        Config.commands["diange"], "guard",
                                        bool, int).grid(column=2, row=0, padx=8)

        # admin perm
        ConfigGUIFactory.getCheckButton(frame_diange_1, _("Admin"),
                                        Config.commands["diange"], "admin",
                                        bool, int).grid(column=3, row=0, padx=8)

        ttk.Label(frame_diange_2, text=_("DG Cooldown (s): ")).grid(column=0, row=0)
        ConfigGUIFactory.getInput(frame_diange_2,Config.commands["diange"],"cooldown",
                                  ConfigGUIFactory.ConvertWithDefault(int,0),
                                  str).grid(column=1, row=0,padx=8)
        ttk.Label(frame_diange_2, text=_("DG Max number: ")).grid(column=2, row=0)
        ConfigGUIFactory.getInput(frame_diange_2,Config.commands["diange"],"limit",
                                  ConfigGUIFactory.ConvertWithDefault(int,128),
                                  str).grid(column=3, row=0,padx=8)


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

        # ========== frame exp ================
        variable = tk.IntVar()
        def tst():
            if variable.get() == 0:
                MatchEngine.HANDLERS.unregister(FindSearchResultEvent,"filtercover")
            else:
                MatchEngine.HANDLERS._register(FindSearchResultEvent,"filtercover",
                                               SkipCover.skip_cover)

        check_button = tk.Checkbutton(frame_etc,
                                      text=_("filter cover"),
                                      variable=variable,
                                      command=tst)
        check_button.grid(column=0, row=0)
from tkinter import ttk
from audiobot.AudioBot import Global_Audio_Bot
import tkinter as tk
import gui
from audiobot.Blacklist import BlacklistItemType, BlacklistItem
from audiobot.event.blacklist import BlacklistUpdateEvent
from audiobot.event.playlist import PlaylistUpdateEvent
from gui.factory.ToolTip import ToolTip
from utils.etc import filterTclSpecialCharacter
from utils.vtranslation import getTranslatedText as _


class BlacklistGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.audio_bot = Global_Audio_Bot
        self.blacklist_tree: ttk.Treeview = None

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("Blacklist"))
        self.audio_bot.blacklist.handlers._register(BlacklistUpdateEvent,
                                                    "blacklistgui.update",
                                                    self.__updateTree)
        self.audio_bot.blacklist.handlers.call(BlacklistUpdateEvent(self.audio_bot.blacklist))

    def createWidgets(self):
        frame_main = ttk.LabelFrame(self.widget, text="Blacklist Manager")
        frame_main.pack(fill="both", expand="yes", padx=8, pady=4)

        frame_blacklist = ttk.Frame(frame_main)
        frame_blacklist.pack(fill=tk.X, expand="yes", side=tk.TOP)

        frame_blacklistadd = ttk.Frame(frame_main)
        frame_blacklistadd.pack(fill=tk.X, expand="yes", side=tk.TOP)

        # ========== blacklist frame ================
        frame_display = ttk.Frame(frame_blacklist)
        frame_display.grid(column=0, row=0, padx=4, pady=4)
        frame_move = ttk.Frame(frame_blacklist)
        frame_move.grid(column=1, row=0, padx=4, pady=4)

        self.blacklist_tree = ttk.Treeview(frame_display, height="13", selectmode="browse")
        self.blacklist_tree["columns"] = ("bantype", "content", "whole")
        self.blacklist_tree.column("#0", width=64, minwidth=32)
        self.blacklist_tree.column("bantype", width=256, minwidth=256)
        self.blacklist_tree.column("content", width=256, minwidth=128)
        self.blacklist_tree.column("whole", width=64, minwidth=128)

        self.blacklist_tree.heading("#0", text="#", anchor=tk.W)
        self.blacklist_tree.heading("bantype", text=_("ban type"), anchor=tk.W)
        self.blacklist_tree.heading("content", text=_("ban content"), anchor=tk.W)
        self.blacklist_tree.heading("whole", text=_("use whole word"), anchor=tk.W)

        self.blacklist_tree.grid(column=0, row=0)
        self.blacklist_tree.bind('<Button-1>', self.__disableTreeSeperator)

        self.blacklist_tree.bind('<ButtonRelease-1>', self.__clearFocusIfEmpty)

        blacklist_del_button = ttk.Button(frame_move, width=3, text="X",
                                          command=lambda: self.audio_bot
                                          .blacklist.remove(self.__getTreeviewFocusIndex()))
        blacklist_del_button.grid(column=0, row=0, pady=2)

        ToolTip(blacklist_del_button, _("delete this blacklist item"))

        # ========== blackadd frame ================
        frame_blacklistadd_0 = ttk.Frame(frame_blacklistadd)
        frame_blacklistadd_0.grid(column=0, row=0, padx=8)

        bantype_var = tk.StringVar()
        bantype_selection = ttk.Combobox(frame_blacklistadd_0,
                                         width=16,
                                         textvariable=bantype_var,
                                         state='readonly')
        bantype_vals = [m.identifier for m in BlacklistItemType.values()]
        bantype_selection['values'] = tuple(bantype_vals)
        bantype_selection.grid(column=0, row=1, padx=8)
        bantype_selection.set(bantype_vals[0])
        bantype_var.set(bantype_vals[0])

        ban_content_var = tk.StringVar()
        ban_content = ttk.Entry(frame_blacklistadd_0,
                                width=32,
                                textvariable=ban_content_var)
        ban_content.grid(column=1, row=1, padx=8, pady=4)

        ban_add_button = ttk.Button(frame_blacklistadd_0,
                                    width=16, text=_("add to blacklist"),
                                    command=lambda :self.audio_bot.blacklist.append(bantype_var.get(),
                                                                                    ban_content_var.get()))
        ban_add_button.grid(column=2, row=1, padx=8, pady=4)

        ttk.Label(frame_blacklistadd_0,text = _("Choose ban type")).grid(column=0, row=0,
                                                                         padx=8, pady=4,
                                                                         sticky = tk.W)
        ttk.Label(frame_blacklistadd_0, text=_("Specify ban content")).grid(column=1, row=0,
                                                                            padx=8, pady=4,
                                                                            sticky = tk.W)

    def __disableTreeSeperator(self, event):
        if self.blacklist_tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def __getTreeviewFocusIndex(self):
        id = self.blacklist_tree.item(self.blacklist_tree.focus())["text"]
        return -1 if id == "" else int(id)

    def __clearFocusIfEmpty(self, event):
        if self.blacklist_tree.identify_region(event.x, event.y) == "nothing":
            self.__clearTreeviewFocus()

    def __clearTreeviewFocus(self):
        self.blacklist_tree.focus('')
        for item in self.blacklist_tree.selection():
            self.blacklist_tree.selection_remove(item)

    def __updateTree(self, event: BlacklistUpdateEvent):
        blacklist = event.blacklist
        self.blacklist_tree.delete(*self.blacklist_tree.get_children())
        for index, item in enumerate(blacklist.blacklist_items):
            item:BlacklistItem
            self.blacklist_tree.insert("", index, text=index, values=(item.bantype.identifier,
                                                                      filterTclSpecialCharacter(item.content),
                                                                      str(item.whole)))

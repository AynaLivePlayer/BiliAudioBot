from tkinter import ttk
from typing import Type

from audiobot import Global_Audio_Bot
import tkinter as tk
import gui
from audiobot.audio import AudioItem
from audiobot.user import SystemUser, DefaultUser
from gui.factory.ToolTip import ToolTip
from sources.base import CommonSource
from sources.base.interface import SearchableSource, AudioBotInfoSource
from utils.vtranslation import getTranslatedText as _

class SearchGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())
        self.audio_bot = Global_Audio_Bot
        self.search_source_class = [s for s in self.audio_bot.selector.sources if issubclass(s,SearchableSource)]
        self.search_result_tree: ttk.Treeview = None
        self.keyword = tk.StringVar()
        self.current_results = []

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("Search"))

    def createWidgets(self):

        frame_main = ttk.LabelFrame(self.widget, text="Search test")
        frame_main.pack(fill="both", expand="yes", padx=8, pady=4)

        frame_search_input  = ttk.Frame(frame_main)
        frame_search_input.pack(fill=tk.X, expand="yes", side=tk.TOP)

        frame_search_result = ttk.Frame(frame_main)
        frame_search_result.pack(fill=tk.X, expand="yes", side=tk.TOP)

        # ========== search input frame ================
        frame_search_input.columnconfigure(0, weight=1)
        frame_search_input.columnconfigure(2, weight=1)

        frame_basic = ttk.Frame(frame_search_input)
        frame_basic.grid(column=1, row=0, padx=8, pady=4)
        # Creating check box for commands
        ttk.Label(frame_basic, text="Keyword or url:") \
            .grid(column=0, row=0, sticky=tk.W, padx=8, pady=4)
        parameter_entry = ttk.Entry(frame_basic, width=64, textvariable=self.keyword)
        parameter_entry.grid(column=0, row=1,
                             padx=8, pady=4)

        # Adding a Button
        action = ttk.Button(frame_basic, width=8, text=_("Search"),command = self.__search)
        action.grid(column=1, row=1)

        # Adding a Button
        action = ttk.Button(frame_basic, width=8, text=_("Add"), command=self.__add)
        action.grid(column=2, row=1)

        # ========== search result frame ================
        frame_search_result.columnconfigure(0, weight=1)
        frame_search_result.columnconfigure(3, weight=1)
        frame_display = ttk.Frame(frame_search_result)
        frame_display.grid(column=1, row=0, padx=4, pady=4)
        frame_tool = ttk.Frame(frame_search_result)
        frame_tool.grid(column=2, row=0, padx=4, pady=4)

        self.search_result_tree = ttk.Treeview(frame_display, height="13", selectmode="browse")
        self.search_result_tree["columns"] = ("title", "artist", "source")
        self.search_result_tree.column("#0", width=64, minwidth=64)
        self.search_result_tree.column("title", width=256, minwidth=256)
        self.search_result_tree.column("artist", width=128+64, minwidth=128)
        self.search_result_tree.column("source", width=128, minwidth=128)

        self.search_result_tree.heading("#0", text="index", anchor=tk.W)
        self.search_result_tree.heading("title", text=_("title"), anchor=tk.W)
        self.search_result_tree.heading("artist", text=_("artist"), anchor=tk.W)
        self.search_result_tree.heading("source", text=_("source"), anchor=tk.W)
        self.search_result_tree.grid(column=0, row=0)

        self.search_result_tree.bind('<Button-1>', self.__disableTreeSeperator)
        self.search_result_tree.bind('<ButtonRelease-1>', self.__clearFocusIfEmpty)

        search_result_add_button = ttk.Button(frame_tool, width=3, text="+",
                                              command = self.__addCurrent)
        search_result_add_button.grid(column=0, row=0, pady=2)

        ToolTip(search_result_add_button, _("add to the playlist"))

        search_result_play_button = ttk.Button(frame_tool, width=3, text="▶",
                                               command  =self.__playCurrent)
        search_result_play_button.grid(column=0, row=1, pady=2)

        ToolTip(search_result_play_button, _("play selected"))

        search_bl_button = ttk.Button(frame_tool, width=3, text="⛒",
                                        command=self.__addCurrentToBlacklist)
        search_bl_button.grid(column=0, row=2, pady=2)

        ToolTip(search_bl_button, _("add to blacklist"))



    def __disableTreeSeperator(self, event):
        if self.search_result_tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def __getTreeviewFocusIndex(self):
        id = self.search_result_tree.item(self.search_result_tree.focus())["text"]
        return -1 if id  == "" else int(id)

    def __clearFocusIfEmpty(self,event):
        if self.search_result_tree.identify_region(event.x, event.y) == "nothing":
            self.__clearTreeviewFocus()

    def __clearTreeviewFocus(self):
        self.search_result_tree.focus('')
        for item in self.search_result_tree.selection():
            self.search_result_tree.selection_remove(item)

    def __getSearchResults(self,keyword):
        results = []
        for s_class in self.search_source_class:
            results.extend(s_class.search(keyword,pagesize=10).results)
        return results

    def __search(self):
        self.main_window.threading_update(self.__updateTree)

    def __add(self):
        self.audio_bot.addAudioByUrl(self.keyword.get(),DefaultUser)

    def __playCurrent(self):
        index = self.__getTreeviewFocusIndex()
        if index == -1:
            return
        self.audio_bot.play(self.current_results[index])

    def __addCurrent(self):
        index = self.__getTreeviewFocusIndex()
        if index == -1:
            return
        self.audio_bot.user_playlist.appendItem(self.current_results[index])

    def __addCurrentToBlacklist(self):
        index = self.__getTreeviewFocusIndex()
        if index == -1:
            return
        self.audio_bot.blacklist.appendPlaylistItem(self.current_results[index])

    def __updateTree(self):
        self.search_result_tree.delete(*self.search_result_tree.get_children())
        if self.keyword.get() == "":
            return
        keyword = self.keyword.get()
        search_results = self.__getSearchResults(keyword)
        self.current_results = [AudioItem(item.source, DefaultUser, "") for item in search_results]
        for index, item in enumerate(search_results):
            source:Type[AudioBotInfoSource,CommonSource] = item.source
            self.search_result_tree.insert("", index, text=index, values=(source.getTitle(),
                                                                          source.getArtist(),
                                                                          source.getSourceName()))
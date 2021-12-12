import time
from tkinter import ttk
import tkinter as tk

import qrcode
from PIL import Image, ImageTk

from audiobot import Global_Audio_Bot
from config import Config
from gui.factory.PlayerProgressBar import PlayerProgressBar
from utils import vwrappers
from utils.vtranslation import getTranslatedText as _
from pyncm import GetCurrentSession,  SetCurrentSession, LoadSessionFromString, DumpSessionAsString
from pyncm.apis import login #GetCurrentLoginStatus, WriteLoginInfo,LoginQrcodeUnikey,LoginQrcodeCheck
import gui


class WYLoginGUI():
    def __init__(self, main_window):
        self.main_window: gui.MainWindow = main_window
        self.widget = ttk.Frame(self.main_window.getTabController())

        self.login_qr = None
        self.empty_image = ImageTk.PhotoImage(Image.new("RGB", (250, 250), (255, 255, 255)))
        self.current_status = tk.StringVar()
        self.uuid = ""

    def initialize(self):
        self.main_window.getTabController().add(self.widget, text=_("Netease Login"))


    def createWidgets(self):
        frame_main = ttk.LabelFrame(self.widget,
                                    text=_("Netease Login"))
        frame_main.grid_columnconfigure(0, weight=1)
        frame_main.grid_columnconfigure(2, weight=1)
        frame_main.pack(fill="both", expand="yes", padx=8, pady=4)
        # ==== Row 1 ====

        frame_row_1 = ttk.Frame(frame_main)
        frame_row_1.grid(column=1, row=0, padx=8, pady=4)

        self.login_qr = ttk.Label(frame_row_1, width=250)
        self.login_qr.grid(column=0, row=0, sticky="news")
        self.__setQrImg(self.empty_image)

        # ==== Row 2 ====

        frame_row_2 = ttk.Frame(frame_main)
        frame_row_2.grid(column=1, row=1, padx=8, pady=4)

        getqr_button = ttk.Button(frame_row_2, width=16, text=_("Get QR"), command=self.__tryLogin)
        getqr_button.grid(column=0, row=0)
        finishqr_button = ttk.Button(frame_row_2, width=16, text=_("Finish QR Scan"), command=self.__checkLogin)
        finishqr_button.grid(column=1, row=0)
        logout_button = ttk.Button(frame_row_2, width=16, text=_("Logout"), command=self.__tryLogout)
        logout_button.grid(column=2, row=0)

        # ==== Row 3 ====

        frame_row_3 = ttk.Frame(frame_main)
        frame_row_3.grid(column=1, row=2, padx=8, pady=4)

        playing_title_label = ttk.Label(frame_row_3, textvariable=self.current_status)
        playing_title_label.grid(column=0, row=0, pady=2, padx=2)
        self.current_status.set("Waiting")

        pyncmcookie = Config.getCookie("netease", "pyncm")
        if pyncmcookie.get("session") is not None:
            try:
                SetCurrentSession(LoadSessionFromString(pyncmcookie.get("session")))
            except:
                pass
        self.__setLoginInfo()

    @vwrappers.TryExceptRetNone
    def __tryLogin(self):
        self.__setQrImg(self.empty_image)
        self.uuid = login.LoginQrcodeUnikey()['unikey']
        url = f'https://music.163.com/login?codekey={self.uuid}'
        img = qrcode.make(url)
        tkimg = ImageTk.PhotoImage(img.resize((250, 250)))
        self.__setQrImg(tkimg)

    def __checkLogin(self):
        rsp = login.LoginQrcodeCheck(self.uuid)
        if rsp['code'] == 803 or rsp['code'] == 800:
            login.WriteLoginInfo(login.GetCurrentLoginStatus())
            Config.getCookie("netease", "pyncm")["session"] = DumpSessionAsString(GetCurrentSession())
            self.__setQrImg(self.empty_image)
            self.__setLoginInfo()


    @vwrappers.TryExceptRetNone
    def __tryLogout(self):
        self.__setQrImg(self.empty_image)
        login.LoginLogout()
        Config.getCookie("netease", "pyncm")["session"] = ""
        self.__setLoginInfo()

    @vwrappers.TryExceptRetNone
    def __setQrImg(self, img):
        self.login_qr.configure(image=img)
        self.login_qr.image = img

    def __isLogin(self):
        return login.GetCurrentSession().login_info["success"]

    def __setLoginInfo(self):
        if self.__isLogin():
            self.current_status.set(_("Login As ")+GetCurrentSession().login_info['content']['profile']['nickname'])
        else:
            self.current_status.set(_("Not Login"))
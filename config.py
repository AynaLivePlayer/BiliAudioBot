import json
from utils import vwrappers


class ConfigFile:
    gui_title = "ヽ(°∀°)点歌姬(°∀°)ﾉ"

    environment = "production"
    # environment = "development"
    version = "Demo0.8.4"

    commonHeaders = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    commonCookies = {}

    system_playlist = {
        "playlist":{"netease":[],
                    "bilibili":[]},
        "song":{"netease":[],
                    "bilibili":[]},
        "random":True,
        "autoskip":True
    }

    output_channel = {
        "web":{"enable":True,
               "port":5000},
        "file":{"enable":True,
                "template":"config/audiobot_template.txt",
                "path":"audiobot_info.txt"}
    }

    commands = {
        "diange": {
            "cooldown":0,
            "limit":128,
            "visitor":True,
            "guard":True,
            "admin":True,
            "fan":None
        },
        "qiege": {
            "self":True,
            "guard":False,
            "admin":False
        },
    }

    audio_device = {"id":"auto"}

    player_volume = 0.32

    default_room = ""

    config_path = "config/config.json"

    cookie_path = "config/cookies.json"

    blacklist_path = "config/blacklist.json"

    translation = {"enable":True,
                   "path":"resource/translation.json"}


    def __init__(self):
        print("Loading config")
        self._loadConfig()
        print("Cookie initialized")
        # structure: {"site":{"identifier":{"cookie1":"value1"}}}
        self.cookies = {}
        self.loadCookie()
        self.blacklist = {}
        self._loadBlacklist()

    @vwrappers.TryExceptRetNone
    def loadCookie(self):
        with open(self.cookie_path,"r") as f:
            jdata = json.loads(f.read().replace(" ", ""))
            for key,val in jdata.items():
                for id, content in val.items():
                    cookie = self.getCookie(key,id)
                    cookie.update(dict(x.split("=") for x in content.split(";") if x != ""))

    @vwrappers.TryExceptRetNone
    def saveCookie(self):
        tmp = self.cookies.copy()
        for host, val in self.cookies.items():
            for id,content in val.items():
                tmp[host][id] = ";".join("{}={}".format(key,val) for key,val in self.cookies[host][id].items())
        with open(self.cookie_path,"w",encoding="utf-8") as f:
            f.write(json.dumps(tmp,indent=2,ensure_ascii=False))

    def getCookiesByHost(self, host):
        if host == "":
            return self.commonCookies
        if self.cookies.get(host) == None:
            self.cookies[host] = {}
            return self.cookies[host]
        return self.cookies.get(host)

    def getCookie(self,host,identifier):
        cookies = self.getCookiesByHost(host)
        if cookies.get(identifier) == None:
            cookies[identifier] = {}
            return self.cookies[host][identifier]
        return cookies[identifier]

    @vwrappers.TryExceptRetNone
    def _loadConfig(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            for key,val in data.items():
                if hasattr(self,key):
                    if isinstance(self.__getattribute__(key),dict):
                        self.__getattribute__(key).update(val)
                    else:
                        self.__setattr__(key,val)

    def saveConfig(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        with open(self.config_path, "w", encoding="utf-8") as f:
            for key,val in data.items():
                if hasattr(self,key):
                    data[key] = self.__getattribute__(key)
            f.write(json.dumps(data,indent=2,ensure_ascii=False))

        self._saveBlacklist()

    @vwrappers.TryExceptRetNone
    def _loadBlacklist(self):
        with open(self.blacklist_path, "r", encoding="utf-8") as f:
            self.blacklist = json.loads(f.read())


    def _saveBlacklist(self):
        with open(self.blacklist_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.blacklist, indent=2, ensure_ascii=False))


Config = ConfigFile()
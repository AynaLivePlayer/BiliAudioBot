import json
from typing import Dict

from utils import vwrappers


class ConfigFile:
    gui_title = "重生之我是欧菲手"

    environment = "production"

    commonHeaders = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    commonCookies = {}

    system_playlist = {
        "playlist":{"netease":[],
                    "bilibili":[]},
        "song":{"netease":[],
                    "bilibili":[]},
        "random":True
    }

    output_channel = {
        "web":{"enable":True,
               "port":5000}
    }

    default_room = ""

    config_path = "config.json"

    cookie_path = "cookies.json"

    def __init__(self):
        print("Loading config")
        self._loadConfig()
        print("Cookie initialized")
        # structure: {"site":{"identifier":{"cookie1":"value1"}}}
        self.cookies = {}
        self.loadCookie()

    def loadCookie(self,path="cookies.json"):
        with open(path,"r") as f:
            jdata = json.loads(f.read().replace(" ", ""))
            for key,val in jdata.items():
                for id, content in val.items():
                    cookie = self.getCookie(key,id)
                    cookie.update(dict(x.split("=") for x in content.split(";") if x != ""))

    def saveCookie(self,path="cookies.json"):
        tmp = self.cookies.copy()
        for host, val in self.cookies.items():
            for id,content in val.items():
                tmp[host][id] = ";".join("{}={}".format(key,val) for key,val in self.cookies[host][id].items())
        with open(path,"w",encoding="utf-8") as f:
            f.write(json.dump(tmp,indent=2))

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
    def _loadConfig(self,path="config.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            for key,val in data.items():
                if hasattr(self,key):
                    if isinstance(self.__getattribute__(key),Dict):
                        self.__getattribute__(key).update(val)
                    else:
                        self.__setattr__(key,val)

    def saveConfig(self,path="config.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        with open(path, "w", encoding="utf-8") as f:
            for key,val in data.items():
                if hasattr(self,key):
                    data[key] = self.__getattribute__(key)
            f.write(json.dumps(data,indent=2))


Config = ConfigFile()
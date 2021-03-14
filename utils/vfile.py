import os
import re
import sys


def parseFilename(filename):
    pattern = r'[\\/:*?"<>|\r\n]+'
    return re.sub(pattern,"-",filename)


def writeToFile(content,route,name,binary=False):
    path = os.path.join(route, parseFilename(name))
    if not os.path.exists(route):
        os.mkdir(route)
    if binary:
        with open(path, "wb+") as f:
            f.write(content)
    else:
        with open(path, "w+",encoding="utf-8") as f:
            f.write(content)

def removeUrlPara(url):
    return url.split("?")[0]

def getSuffixByUrl(url):
    return removeUrlPara(url).split(".")[-1]

def getFileNameByUrl(url):
    return removeUrlPara(url).split("/")[-1]


def getResourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
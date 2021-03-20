import json
import os
import traceback

from config import Config
from utils import vfile

TRANSLATION_DICT = {}

try:
    with open(vfile.getResourcePath(Config.translation["path"]),"r",encoding="utf-8") as f:
        TRANSLATION_DICT = json.loads(f.read())
except:
    traceback.print_exc()
    pass


def getTranslatedText(text):
    if TRANSLATION_DICT.get(text) is None:
        TRANSLATION_DICT[text] = text
        if Config.environment == "development":
            vfile.writeToFile(json.dumps(TRANSLATION_DICT,indent=4,ensure_ascii=False),
                          os.path.dirname(Config.translation["path"]),
                          os.path.basename(Config.translation["path"]))
    if Config.translation["enable"]:
        return TRANSLATION_DICT[text]
    else:
        return text
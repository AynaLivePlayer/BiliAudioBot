import config
from audiobot.commands import diange,qiege

from os import getcwd
from os.path import  basename, isfile, join
import glob,importlib

for f in glob.glob(join(getcwd(),config.Config.addon_cmd_path, "*.py")):
    name = basename(f)[:-3:]
    if isfile(f):
        print(f)
        importlib.import_module("addons.cmd." + name)
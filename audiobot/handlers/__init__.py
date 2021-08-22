import config

from os import getcwd
from os.path import  basename, isfile, join
import glob,importlib


for f in glob.glob(join(getcwd(), config.Config.addon_handler_path, "*.py")):
    name = basename(f)[:-3:]
    if isfile(f):
        importlib.import_module("addons.handler." + name)
from utils import vfile
# import os
# #os.environ['no_proxy'] = '*'
vfile.registerEnvironmentPath()
import nest_asyncio
nest_asyncio.apply()

from utils.etc import patchPyncm
patchPyncm()

from aiohttp import web
from backend.localfileserver import LocalFileWriterServer
from config import Config

from gui import MainWindow
from backend.aioserver import app as aioserver_app
import asyncio
async def mainloop(loop):
    a = MainWindow(loop=loop)
    task = [loop.create_task(a.start())]
    if Config.output_channel["web"]["enable"]:
        app = aioserver_app
        task.append(loop.create_task(run_backend(app)))
    if Config.output_channel["file"]["enable"]:
        lfs = LocalFileWriterServer()
        task.append(loop.create_task(lfs.start()))
    await asyncio.wait(task, return_when=asyncio.FIRST_COMPLETED)
    try:
        asyncio.get_event_loop().stop()
    except:
        pass

async def mainloop_gui_only(loop):
    a = MainWindow(loop=loop)
    task = [loop.create_task(a.start())]
    await asyncio.wait(task, return_when=asyncio.FIRST_COMPLETED)
    try:
        asyncio.get_event_loop().stop()
    except:
        pass


async def run_backend(app):
    web.run_app(app, host='127.0.0.1', port=Config.output_channel["web"]["port"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainloop(loop))
    try:
        Config.saveConfig()
    except:
        pass

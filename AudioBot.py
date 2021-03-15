import os

from aiohttp import web

from config import Config

os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]

from gui import MainWindow
from backend import aioserver
import asyncio
import nest_asyncio

nest_asyncio.apply()


async def mainloop(loop):
    a = MainWindow(loop=loop)
    app = aioserver.app
    task = [loop.create_task(a.start()),
            loop.create_task(run_backend(app))]
    await asyncio.wait(task, return_when=asyncio.FIRST_COMPLETED)
    await app.cleanup()
    await app.shutdown()
    try:
        asyncio.get_event_loop().stop()
    except:
        pass


async def run_backend(app):
    web.run_app(app, host='127.0.0.1', port=Config.web_port)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainloop(loop))

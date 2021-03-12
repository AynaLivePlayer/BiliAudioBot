import os
from threading import Thread

from aiohttp import web

os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]

from gui import MainWindow
from backend import aioserver
import asyncio
import nest_asyncio
nest_asyncio.apply()


async def mainloop(loop):
    a = MainWindow()

    await asyncio.create_task(a.start(),
                              run_backend())

def run_backend():
    backend = aioserver.app
    web.run_app(backend, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainloop(loop))
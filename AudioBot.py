import os
from threading import Thread

os.environ["PATH"] = os.getcwd() + os.pathsep + os.environ["PATH"]

from gui import MainWindow
import asyncio
import nest_asyncio
nest_asyncio.apply()


async def mainloop(loop):
    a = MainWindow()
    await asyncio.create_task(a.start())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainloop(loop))
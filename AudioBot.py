import asyncio

from gui import MainWindow
import nest_asyncio
nest_asyncio.apply()

async def mainloop(loop):
    a = MainWindow(loop=loop)
    await asyncio.gather(a.start())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainloop(loop))
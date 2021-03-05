import asyncio

from gui import MainWindow
import nest_asyncio
nest_asyncio.apply()

async def mainloop():
    a = MainWindow()
    await asyncio.gather(a.start())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(mainloop())
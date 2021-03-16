import aiohttp
from aiohttp import web
import os

from backend import audiobot_socket
from config import Config
from utils import vfile

ENV = Config.environment
DIST_DIR = vfile.getResourcePath("./frontend/dist")

app = web.Application()
routes = web.RouteTableDef()


@routes.get("/ws/audiobot")
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    audiobot_socket.websockets.append(
        ws
    )
    await audiobot_socket.sendInitialData(ws)
    async for msg in ws:
        msg:aiohttp.WSMessage
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    audiobot_socket.websockets.remove(ws)
    print('websocket connection closed')
    return ws

@routes.get("/")
@routes.get("/{path:.*}")
async def vue_redirecting(request: web.Request):
    try:
        path = request.match_info["path"]
    except:
        path = ""
    if ENV == "development":
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/{}'.format(path)) as resp:
                return web.Response(text=await resp.text(),
                                    content_type=resp.content_type)
    else:
        if path.startswith("static") or path == "":
            path = os.path.join(DIST_DIR, "index.html") if path == "" else os.path.join(DIST_DIR, path)
            if not os.path.exists(path):
                return web.Response(status=404)
            with open(path, "r", encoding="utf-8") as f:
                return web.Response(text=f.read(),
                                    content_type=vfile.getFileContentType(path))

        with open(os.path.join(DIST_DIR, "index.html"), "r", encoding="utf-8") as f:
            return web.Response(text=f.read(),
                                content_type=vfile.getFileContentType(path))

app.router.add_routes(routes)

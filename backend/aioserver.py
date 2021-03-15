import aiohttp
from aiohttp import web
import os

from utils import vfile

ENV = "development"
DIST_DIR = "./frontend/dist"

app = web.Application()
routes = web.RouteTableDef()
# aiohttp_jinja2.setup(app,
#                      loader=jinja2.FileSystemLoader('./frontend/dist'))


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
        path = os.path.join(DIST_DIR, "index.html") if path == "" else os.path.join(DIST_DIR, path)
        if not os.path.exists(path):
            return web.Response(status=404)
        with open(path, "r", encoding="utf-8") as f:
            return web.Response(text=f.read(),
                                content_type=vfile.getFileContentType(path))


app.router.add_routes(routes)

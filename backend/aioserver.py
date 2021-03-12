import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
ENV = "development"

app = web.Application()
routes = web.RouteTableDef()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('./frontend/dist'))

@routes.get("/")
@routes.get("/{path:.*}")
async def vue_redirecting(request:web.Request):
    try:
        path = request.match_info["path"]
    except:
        path = ""
    if ENV == "development":
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/{}'.format(path)) as resp:
                return web.Response(text=await resp.text(),
                                    content_type= resp.content_type)
    return aiohttp_jinja2.render_template('index.html',
                                              request)

app.router.add_routes(routes)

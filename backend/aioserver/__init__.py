from aiohttp import web
from config import Config
from utils import vfile

ENV = Config.environment
DIST_DIR = vfile.getResourcePath("./frontend/dist")

app = web.Application()
routes = web.RouteTableDef()

from backend.aioserver import router_handlers

app.add_routes(routes)
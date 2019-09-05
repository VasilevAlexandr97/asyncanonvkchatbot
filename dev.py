from aiohttp import web
from bot import init_app

app = init_app()
web.run_app(app)

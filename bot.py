from aiohttp import web
import aiohttp
import asyncpgsa
from view import bot
from parsers import ParserVkRequest


async def index(request):
    pr = ParserVkRequest(request)
    request_type = await pr.get_type()
    if request_type == 'confirmation':
        return web.Response(text='b5996629')
        # return web.Response(text='12a0d13d')
    elif request_type == 'message_new':
        vkid = await pr.get_user_id()
        payload = await pr.get_payload()
        message = await pr.get_message()
        attachment = await pr.get_attachment()
        await bot(request, vkid, payload, message, attachment)
        return web.Response(text='ok')

def setup_routes(app):
    app.router.add_route('POST', '/', index)


async def init_app():
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_close)
    return app


async def on_start(app):
    app['db'] = await asyncpgsa.create_pool(
        host="localhost",
        port="5432",
        database="database",
        user="user",
        password="password"
    )


async def on_close(app):
    await app['db'].close()
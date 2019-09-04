"""
演示如何结合UDP服务和websocket
"""
import asyncio
import aiohttp_jinja2
from aiohttp import web
import jinja2
import sys

event = asyncio.Event()
message = None


class MyServerUdpEchoProtocol:

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        global message
        print('Data received:', data, addr)
        message = data.decode()
        event.set()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print('stop', exc)


async def index(request):
    global event
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws_current.prepare(request)

    while True:
        await event.wait()
        await ws_current.send_str(message)
        event = asyncio.Event()


async def init_app():

    app = web.Application()

    app['websockets'] = {}

    app.on_shutdown.append(shutdown)

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader(__loader__.name, 'templates'))

    app.router.add_get('/', index)

    loop = asyncio.get_event_loop()
    asyncio.Task(loop.create_datagram_endpoint(
        MyServerUdpEchoProtocol, local_addr=('0.0.0.0', 6066)))

    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main():
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
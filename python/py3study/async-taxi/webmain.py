import asyncio
import aiohttp_jinja2
from aiohttp import web
import jinja2
from aworld import *
import json
import os.path


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Point):
            return {'x':o.x, 'y':o.y}
        if isinstance(o, Vehicle):
            return {
                'id': o.id,
                'location': o.location,
                'status': o.status,
                'segments': o.segments,
                'heading': o.heading,
            }
        return json.JSONEncoder.encode(self, o)


def my_json_dumps(o):
    return json.dumps(o, cls=MyJSONEncoder)


center = Point(104.068138, 30.661796)
runner = LoopRunner(main_process=main_process, actors=[
        Vehicle(id_=id, location=center.random(2000))
        for id in range(1, 2)
    ])


async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})

    await ws_current.prepare(request)

    while not ws_current.closed:
        await ws_current.send_json(runner.actors, dumps=my_json_dumps)
        await asyncio.sleep(0)


async def init_app():

    app = web.Application()

    app['websockets'] = {}

    app.on_shutdown.append(shutdown)

    asyncio.create_task(runner.main())

    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('webmain', 'templates'))

    app.router.add_get('/', index)
    app.router.add_static('/static', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

    # web.static('/static', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), show_index=True)

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
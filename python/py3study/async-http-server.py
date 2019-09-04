from aiohttp import web
from PIL import Image, ImageDraw
import io
import mimetypes
import asyncio


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def watermark(request):
    file = 'a.jpg'
    im = Image.open(file)

    d = ImageDraw.Draw(im)
    d.text((100, 100), "Hello", fill=(255, 255, 255, 128))

    bytes = io.BytesIO()
    im.save(bytes, 'JPEG')

    data = bytes.getvalue()
    resp = web.StreamResponse()
    await resp.prepare(request)

    resp.content_type = mimetypes.guess_type(file)
    resp.content_length = len(data)

    await resp.write(data)
    return resp


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/watermark', watermark),
                ])

if __name__ == '__main__':
    web.run_app(app)
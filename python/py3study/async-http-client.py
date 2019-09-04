import asyncio
import aiohttp
import time


async def fetch(session, url):
    async with session.get(url=url, ssl=url.startswith('https')) as response:
        return await response.text()


async def get(url):
    print(url, 1)
    async with aiohttp.ClientSession() as session:
        print(url, 2)
        s = await fetch(session, url)
        print(url, 3)


async def main():
    with open('data/links.txt', 'rt') as fp:
        for url in fp.readlines():
            await get(url)

t = time.time()
asyncio.run(main(), debug=True)
print(time.time() - t)
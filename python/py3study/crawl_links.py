import time
import requests
from multiprocessing import Pool
from concurrent import futures
import asyncio
import aiohttp


def timeit(f):
    def _wrapper():
        t = time.time()
        f()
        print('time', f.__name__, time.time() - t)
    return _wrapper


links = None
with open('data/links.txt', 'rt') as fp:
    links = fp.readlines()


@timeit
def synchronize():
    for url in links:
        requests.get(url)


@timeit
def process():
    with Pool(4) as p:
        p.map(requests.get, links)


@timeit
def thread():
    with futures.ThreadPoolExecutor(4) as p:
        p.map(requests.get, links)


@timeit
def asyncs():
    async def get(url, session):
        async with session.get(url=url, ssl=url.startswith('https')) as response:
            if response.reason == 'OK':
                s = await response.read()
                # print(url, len(s))
            else:
                print(url, response.reason)
                # raise IOError(response.reason)

    async def main():
        # await get('https://www.163.com')
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(get(url.strip(), session)) for url in links]
            await asyncio.gather(*tasks)

    asyncio.run(main(), debug=True)

synchronize()
process()
thread()
asyncs()




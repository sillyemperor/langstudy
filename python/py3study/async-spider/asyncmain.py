import asyncio
import aiohttp
from bs4 import BeautifulSoup
import counter

c = counter.counter()

next(c)


queue = None


async def get(url):
    global c, queue
    if not url.startswith('http'):
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, ssl=url.startswith('https')) as response:
                s = await response.text()
                # print(url)
                c.send(len(s))
                bs = BeautifulSoup(s, features="html.parser")
                urls = [i.attrs['href'] if 'href' in i.attrs else '' for i in bs.find_all('a')]
                print(url, len(urls))
                for i in urls:
                    await queue.put(i)
    except:
        pass


async def crawl():
    global queue
    while True:
        url = await queue.get()

        await get(url)
        queue.task_done()


async def main():
    global queue
    queue = asyncio.Queue()
    await queue.put('http://www.163.com')

    # 使用多个task可以明显提高效率
    tasks = [asyncio.create_task(crawl()) for _ in range(2)]

    await queue.join()

    for task in tasks:
        task.cancel()

asyncio.run(main())

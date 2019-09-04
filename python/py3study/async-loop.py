import asyncio
import random


async def loops(id, n):
    for i in range(n):
        print('loops', id, i)


async def loopa(id, n):
    for i in range(n):
        await asyncio.sleep(random.randint(0, 3))
        print('loopa', id, i)


async def main():
    tasks = [asyncio.create_task(loops(i, 10)) for i in range(3)]
    for t in tasks:
        await t

    tasks = [asyncio.create_task(loopa(i, 10)) for i in range(3)]
    for t in tasks:
        await t


asyncio.run(main())
import asyncio
import time


async def dosomthing(t):
    # await asyncio.sleep(t)
    for i in range(t):
        await asyncio.sleep(0)


async def sleeep(id_, t):
    print('Start', id_)
    await dosomthing(t)
    # time.sleep(t)
    print('End', id_)


async def main():
    t = time.time()
    await asyncio.gather(*[
        sleeep('1', 2),
        sleeep('2', 3),
        sleeep('3', 1),
    ])
    print('gather', time.time() - t)

    t = time.time()
    for i in [sleeep('1', 2),sleeep('2', 3),sleeep('3', 1)]:
        await i;
    print('for loop', time.time() - t)


asyncio.run(main(), debug=True)


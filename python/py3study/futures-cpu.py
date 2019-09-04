"""
GIL的存在，使得CPU密集型的计算无法获得多线程的好处，只能使用多进程，至于携程完全没有作用
"""
import time
import hashlib
from concurrent import futures
import asyncio

s = b'1234567890'*1000000
print('Size', len(s))
m = hashlib.sha256()


def foo(_):
    m.update(s)
    m.digest()


async def afoo():
    m.update(s)
    m.digest()


loops = range(1, 20)

t = time.time()
list(map(foo, loops))
print('sync', time.time() - t)


t = time.time()
with futures.ThreadPoolExecutor(4) as ex:
    ex.map(foo, loops)
print('thread', time.time() - t)


t = time.time()
with futures.ProcessPoolExecutor(4) as ex:
    ex.map(foo, loops)
print('process', time.time() - t)


async def amain():
    await asyncio.gather(*[afoo() for _ in loops])

t = time.time()
asyncio.run(amain())
print('async', time.time() - t)
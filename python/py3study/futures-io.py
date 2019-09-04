"""
GIL在IO或者time.sleep等调用时会被释放，因此含有这类调用，例如访问网页，的函数更适合用多线程
"""
import time
from concurrent import futures


def foo(t):
    time.sleep(t)


t = time.time()
for i in map(foo, [1, 2, 3]):
    pass
print('sync', time.time() - t)


t = time.time()
with futures.ThreadPoolExecutor(10) as ex:
    ex.map(foo, [1, 2, 3])
print('thread', time.time() - t)


t = time.time()
with futures.ProcessPoolExecutor(10) as ex:
    ex.map(foo, [1, 2, 3])
print('process', time.time() - t)



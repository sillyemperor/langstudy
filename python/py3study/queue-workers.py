import queue
import os
import threading

q = queue.Queue()


def producer():
    for i in range(100):
        q.put(f'{threading.current_thread().name}-{i}')


def consumer():
    with open('out.txt', 'w+') as fp:
        while True:
            item = q.get()
            if item is None:
                break
            fp.write(item + os.linesep)


worker = [threading.Thread(target=producer) for _ in range(2)]
[i.start() for i in worker]

master = threading.Thread(target=consumer)
master.start()

[i.join() for i in worker]
q.put(None)
master.join()







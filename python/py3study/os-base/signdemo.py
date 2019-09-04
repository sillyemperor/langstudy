import signal
import time
import os
import threading

print(os.getpid())
print(threading.currentThread().ident)

SIGNS = []
def sign_handler(s, f):
    print('Receive ', s, f, threading.currentThread().ident)
    SIGNS.append(s)


signal.signal(signal.SIGHUP, sign_handler)

while True:
    time.sleep(1)
    print(SIGNS)

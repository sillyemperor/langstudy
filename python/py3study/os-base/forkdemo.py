import os

name = 'wj'

if __name__ == '__main__':
    print('%d is parent' % os.getpid())
    pid = os.fork()
    if pid != 0:
        print('%d born %d'%(os.getpid(), pid))
    else:
        print(f'{os.getpid()} borned')

    print('%d say Hello'%os.getpid())

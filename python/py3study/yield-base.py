"""
yield 将控制交给函数调用者
"""


def foo():
    yield 1
    yield 2
    yield 3


for i in foo():
    print(i)

f = foo()

print('1', next(f))
print('2', next(f))
print('3', next(f))
# print('4', next(f))


def foo2(x):
    y = yield x
    print('foo2', x+y)
    yield y


f = foo2(12)

print(next(f))
print(f.send(106))


def foo3(n):
    y = 0
    for i in range(n):
        y = yield i + y


f = foo3(3)


print(next(f))
print(f.send(6))
print(f.send(6))



def foo():
    for i in range(100):
        yield i


def foo2():
    yield from foo()


f = foo()

print(f)
print(iter(f))

for i in f:
    print(i)


f = foo2()


for i in f:
    print(i)
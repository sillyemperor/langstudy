
def loop(id, n):
    for i in range(n):
        yield id, i


tasks = [loop(i, 3) for i in range(10)]


while True:
    for t in tasks:
        print(next(t))



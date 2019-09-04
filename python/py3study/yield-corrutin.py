def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        print('inside: return and wait')
        term = yield average
        print('inside: term', term)
        total += term
        count += 1
        average = total/count


a = averager()

print('outside: call next')
print('outside:', next(a))
print()

print('outside: send', 10)
print('outside:', a.send(10))
print()

print('outside: send', 13.8)
print('outside:', a.send(13.8))
print()

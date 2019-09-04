import helloworld
import geom
import time

print(geom.merc_distance(103.966866, 30.562932, 103.961372, 30.559606))
print(helloworld.merc_distance(103.966866, 30.562932, 103.961372, 30.559606))

t = time.time()
for _ in range(10000000):
    helloworld.merc_distance(103.966866, 30.562932, 103.961372, 30.559606)
print(time.time() - t)

t = time.time()
helloworld.demo()
print(time.time() - t)


t = time.time()
for _ in range(10000000):
    geom.merc_distance(103.966866, 30.562932, 103.961372, 30.559606)
print(time.time() - t)


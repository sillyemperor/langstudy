import logging
import collections
import random
import asyncio
import aiohttp
from geom import *
from vector import *
import json

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)-15s %(message)s')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'{self.x} {self.y}'

    def random(self, radius1, radius2=None):
        x, y = ll2m(self.x, self.y)
        sx = 0.5 - random.random() > 0 and 1 or -1
        sy = 0.5 - random.random() > 0 and 1 or -1
        d = random.randint(radius1, radius2 if radius2 else radius1)
        return Point(*m2ll(x + sx * d, y + sy * d))

    def geodistance(self, other):
        return merc_distance(self.x, self.y, other.x, other.y)


class LoopRunner:
    def __init__(self, actors, main_process):
        self._loops = 0
        self._async_funcs = []
        self.actors = actors
        self.main_process = main_process

    @property
    def loop(self):
        return self._loops

    async def main(self):
        logging.info('Start')
        while True:
            self._loops += 1
            await self.main_process(self)
            await asyncio.gather(*[self._update(i) for i in self.actors])
        logging.info('End')

    def run(self):
        asyncio.run(self.main())

    async def _update(self, actor):
        try:
            await getattr(actor, 'update')(self)
        except Exception as err:
            pass
            # traceback.print_exc()

#                    -----finish order-----
#                    |                    |
#                    |                    |
#                    V                    |
#Hang Up--on duty-->Drift--got order-->Delivery
#     A              |
#     |              |
#     |           off duty
#     |              |
#     |              |
#     ----------------
VehicleStatus = ('Hang Up', 'Drift', 'Delivery', )


amap_key = '2f8845cd6f5ee92747489b37619cefad'

async def get_direction(origin, destination):
    async with aiohttp.ClientSession() as session:
        async with session.get(url='https://restapi.amap.com/v3/direction/driving', ssl=True, params=dict(
                key=amap_key,
                origin='{lng},{lat}'.format(lng=origin.x, lat=origin.y),
                destination='{lng},{lat}'.format(lng=destination.x, lat=destination.y),
        )) as response:
            o = await response.json()
            if not o['status']:
                raise Exception(o['info'])
            if not 'count' in o or not o['count']:
                raise Exception('no data')
            steps = o['route']['paths'][0]['steps']
            if not steps:
                raise Exception('no steps')
            distance = float(o['route']['paths'][0]['distance'])
            segments = []
            last_stop = None
            for step in steps:
                for stop in step['polyline'].split(';'):
                    if last_stop:
                        segments.append((
                            Point(*[float(i) for i in last_stop.split(',')]),
                            Point(*[float(i) for i in stop.split(',')]),
                        ))
                    last_stop = stop
            return segments, distance


class Order:
    def __init__(self, id_, start, end):
        self.id = id_
        self.start = start
        self.end = end

    def __str__(self):
        return 'Order(%s)'%self.id


seconds_loop = 0.5


async def main_process(ctx):
    for i in filter(lambda x: x.status == VehicleStatus[0], ctx.actors):
        await i.start_drift()

    for i in filter(lambda x: x.status == VehicleStatus[1], ctx.actors):
        if ctx.loop % 1000 == 0:
            await i.start_order()
        await i.drift()

    for i in filter(lambda x: x.status == VehicleStatus[2], ctx.actors):
        await i.check_order()

    # if ctx.loop > 700:
    #     for i in filter(lambda x: x.status == VehicleStatus[1], ctx.actors):
    #         if i.available:
    #             i.off_duty()


class Vehicle:
    def __init__(self, id_, location):
        self.id = id_
        self.location = location
        self._destination = None
        self._status = VehicleStatus[0]
        self._order = None

        self._segments = None
        self._distance = None
        self._segment_index = 0

    @property
    def segments(self):
        return self._segments

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def heading(self):
        if self._segments:
            segment = self._segments[self._segment_index]
            x1, y1 = ll2m(self.location.x, self.location.y)
            x2, y2 = ll2m(segment[1].x, segment[1].y)

            return angle(vec((x1, y1), (x1, y1+1000)), vec((x1, y1), (x2, y2)))
        return 0

    async def set_destination(self, value):
        self._destination = value
        self._segments, self._distance = await get_direction(self.location, self._destination)
        self._segment_index = 0

    @property
    def available(self):
        return self.status == VehicleStatus[1] and not self._order

    async def start_drift(self):
        self.status = VehicleStatus[1]
        await self.set_destination(self.location.random(1000))

    async def drift(self):
        if not self._segments:
            await self.set_destination(self.location.random(1000))

    def off_duty(self):
        self.status = VehicleStatus[0]

    async def start_order(self):
        order = Order(id_=0, start=self.location, end=self.location.random(random.randint(1000, 5000)))
        self._order = order
        self.status = VehicleStatus[2]
        await self.set_destination(order.end)

    async def check_order(self):
        if self._order:
            d = self._order.end.geodistance(self.location)
            if d <= 10 or not self._segments:
                self._order = None
                await self.start_drift()
                logging.info('Done order')

    def update(self, cxt):
        if self._segments:
            segment = self._segments[self._segment_index]
            x, y = ll2m(self.location.x, self.location.y)
            v = vec((x, y), ll2m(segment[1].x, segment[1].y))
            n = v.normal
            if not n:
                return
            remain_distance = v.distance#merc_distance(self.location.x, self.location.y, segment[1].x, segment[1].y)

            speed = random.randint(10, 20) # m/s
            distance = speed * seconds_loop
            if distance >= remain_distance:
                distance = remain_distance
                self._segment_index += 1
                if self._segment_index >= len(self._segments):
                    self._segments = None
            self.location = Point(*m2ll(x + n[0] * distance, y + n[1] * distance))
        logging.info(f'id={self.id} distance={self.location.geodistance(self._destination)} location={self.location} segments={self._segments}')


if __name__ == '__main__':
    center = Point(104.068138, 30.661796)
    LoopRunner(main_process=main_process, actors=[
        Vehicle(id_=id, location=center.random(2000))
        for id in range(1, 2)
    ]).run()
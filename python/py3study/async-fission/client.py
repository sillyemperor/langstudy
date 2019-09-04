import asyncio
import json
import time

clients = []


class Client:
    def __init__(self, id_):
        self.id = id_
        self.writer = None

    def sends(self, s):
        self.writer.write(s.encode())
        print('>', self.id, s)

    def register(self):
        self.sends(json.dumps(dict(
            client=self.id
        )))

    async def start(self):
        self.reader, self.writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
        self.register()

    def sendto(self, id_):
        self.sends(json.dumps({
            "from": self.id,
            "to": id_,
            "depth": 3,
            "send_ts": time.time(),
        }))

    async def __call__(self):
        data = await self.reader.read(100)
        obj = json.loads(data.decode())
        obj['receive_ts'] = time.time()
        print('<', self.id, obj)


async def call(client):
    await client()


clients = [Client(i) for i in range(3)]


async def main_loop():
    for c in clients:
        await c.start()

    clients[0].sendto(1)

    clients[1].sendto(2)

    clients[2].sendto(0)

    await asyncio.gather(*[call(c) for c in clients])

    # while True:
    #     await asyncio.gather(*[call(c) for c in clients])


asyncio.run(main_loop())





import asyncio
import json

clients = {}


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('<', message)
        obj = json.loads(message)

        if 'client' in obj:
            clients[obj['client']] = self.transport
        elif 'to' in obj and obj['to'] in clients:
            clients[obj['to']].write(data)
            print('>', message)


async def main():
    loop = asyncio.get_running_loop()

    async with await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888) as server:
        await server.serve_forever()

asyncio.run(main())
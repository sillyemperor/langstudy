import asyncio
import json


class RegisterCenterServerProtocol(asyncio.Protocol):
    listener_list = []

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        peername = self.transport.get_extra_info('peername')
        message = data.decode()
        print('Data received: {!r}'.format(message))

        response = 'ok'

        parts = message.rsplit()

        print(parts)

        if '/r' == parts[0]:# register port
            self.listener_list.append(dict(zip(('ip', 'port'),(peername[0], parts[1]))))
        elif '/l' == parts[0]:# list all listeners
            response = json.dumps(self.listener_list)
        elif '/q' == parts[0]:# quit
            self.transport.close()
            response = None

        print('Response', response)
        if response is not None:
            self.transport.write(response.encode())


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: RegisterCenterServerProtocol(),
        '0.0.0.0', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())


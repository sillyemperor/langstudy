import asyncio


async def tcp_echo_client(reader, writer, message):
    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')


class RobotServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    reader, writer = await asyncio.open_connection(
        '39.106.97.131', 8888)

    await tcp_echo_client(reader, writer, f'/r 8899')

    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: RobotServerProtocol(),
        '0.0.0.0', 8899)

    async with server:
        await server.serve_forever()

asyncio.run(main())

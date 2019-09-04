import asyncio


async def tcp_echo_client(reader, writer, message):
    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    # print('Close the connection')
    # writer.close()
    # await writer.wait_closed()


async def main():
    reader, writer = await asyncio.open_connection(
        '39.106.97.131', 8888)

    await tcp_echo_client(reader, writer, f'/l')

asyncio.run(main())

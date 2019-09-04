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
        '182.150.137.197', 8899)

    for i in range(10):
        await tcp_echo_client(reader, writer , f'{i}')

    # await asyncio.gather(*[
    #     tcp_echo_client(*await asyncio.open_connection(
    #     '127.0.0.1', 8888), f'{i}')
    #     for i in range(10)
    # ])

asyncio.run(main())

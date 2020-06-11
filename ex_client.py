from asyncio import open_connection
from asyncio import get_event_loop
from utils import log, input_log, SERVER_IP, SERVER_PORT
from struct import unpack


async def tcp_echo_client(loop):

    stream_in, stream_out = await open_connection(
        SERVER_IP, SERVER_PORT, loop=loop)

    log('Connection opened')
    log('Waiting for confirmation...')
    data = await stream_in.read(1024)
    accepted = unpack('?', data)[0]

    if accepted:
        log('Connection accepted')
        name = input_log('Enter your nickname: ')
        stream_out.write(name.encode())
        await stream_out.drain()

        data = input_log(f'Hey {name}, pick a number: ')
        stream_out.write(data.encode())
        await stream_out.drain()

        log('Waiting for the winner...')
        data = await stream_in.read(1024)
        won = unpack('?', data)[0]

        if won:
            log('You won!')
        else:
            log('You lost.')
    else:
        log(f'Connection denied')
        log(f'The maximum number of players already reached')

    log('Closing the socket...')
    stream_out.close()
    log('Socket closed\n')


loop = get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()

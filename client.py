from asyncio import open_connection
from asyncio import get_event_loop
from utils import SERVER_IP, SERVER_PORT
from protal import ClientProtal, DISCONNECT
from protal import DATA, NAME, COLOUR, ROOM_INFO, WAIT
from protal import PAINT, ORDER, MATRIX, WINNER, EXTRA_TURN
from game import Matrix


async def tcp_echo_client(custom_loop):

    protocol = ClientProtal()

    stream_in, stream_out = await open_connection(
        SERVER_IP, SERVER_PORT, loop=custom_loop)

    # print('opened..')
    current_round = 1
    while True:
        stream = await stream_in.read(1024)
        event, data = protocol.recv(stream)
        # print(event, data)

        if event == DISCONNECT:
            if data is not None:
                matrix = Matrix.get_coloured_matrix(data[MATRIX])
                print('\n\n-----\nFinal Round\n')
                print(matrix)
                if data[WINNER]:
                    print('You won :)')
                else:
                    print('You lost :(')
            else:
                print('Server not allowing more players')
            stream_out.close()
            break
        elif event == DATA:
            stream = enter_info(protocol, data)
            stream_out.write(stream)
            await stream_out.drain()
        elif event == PAINT:
            player_colour = protocol.get_colour()
            colours = protocol.get_colours()
            player_id = protocol.get_id()
            order = data[ORDER]
            extra_turn = data.get(EXTRA_TURN, False)
            matrix = Matrix.get_coloured_matrix(data[MATRIX])

            print(f'\n\n-----\nRound {current_round}')
            current_round += 1
            print(f'\nYou are player {player_id}')

            if extra_turn:
                print(f'You got an extra turn!')
                print(f'This EXTRA round order is {order}')
                current_round -= 1
            else:
                print(f'This round order is {order}')

            print(f'\nMatrix\n{matrix}')
            print(f'Your colour is {player_colour}')
            colour = int(input(f'Pick a colour to paint: {colours} '))
            row = int(input(f'Pick a row to paint: [{1} ~ {len(data[MATRIX])}] ')) - 1
            col = int(input(f'Pick a column to paint: [{1} ~ {len(data[MATRIX])}] ')) - 1
            stream = protocol.pack_painting(colour, row, col)
            # stream = protocol.pack_painting(1, 1, 1)
            stream_out.write(stream)
            await stream_out.drain()
        elif event == WAIT:
            print('Waiting for other players...')
        else:
            raise RuntimeError(f'Unknown event {hex(event)}')


def enter_info(protocol, data):
    name, colour, size = [None] * 3
    if NAME in data:
        name = input('Enter your nick: ')
        # name = 'arthur'
    if COLOUR in data:
        print('Available colours:')
        for colour in protocol.get_colours():
            print(colour)
        colour = int(input('Pick a colour: '))
        # colour = protocol.get_colours()[0]
    if ROOM_INFO in data:
        size = int(input('Enter the room size: '))
        # size = 2

    return protocol.pack_info(name, colour, size)


loop = get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()

# each player owns a colour (blue, red, black, green, etc)
# each player chooses a colour to paint one spot of the matrix
# each player can bet any of the colours
# as soons as every spot is painted, the dominating colour wins the game
#
# each round, a new player bets a colour first
# the order of betting changes every round (clock-wise)
# every round, each player bets a colour in a spot
# if a colour is bet in a blank space, the colour bet is painted
# if two players bet a colour in the same spot, the last player gets the spot
# if a player bets a colour in a spot with that same colour, \
# | the colour is removed from that spot

# a onda é ter duas tasks "mães"... uma é o próprio server, que chama aquela \
# | função async ali toda vez que alguém conecta... a outra é uma que fica \
# | observando o status do server (crie uma abstração pra guardar os clientes \
# | conectados com suas streams, respostas, etc)... assim que o server ficar \
# | em um estado X é só tu loopar nos clientes e mandar a resposta
# asyncio.create_task pode abrir sua cabeça aí

from asyncio import get_event_loop, start_server
from utils import log, SERVER_IP, SERVER_PORT, TRUE, FALSE


class Server:
    def __init__(self, max_players):
        loop = get_event_loop()
        self._max_players = max_players
        self._players = {}
        self._counter = 0
        self._numbers = 0

        coroutine = start_server(
            self._discover_players, SERVER_IP, SERVER_PORT, loop=loop)
        server = loop.run_until_complete(coroutine)

        log(f'Server running on {SERVER_IP}:{SERVER_PORT}\n')
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            # Close the server
            log('Closing the server...', new_line=True)
            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()
        finally:
            log('Server closed')

    async def start(self):
        winner = None
        winner_number = 0
        for player_id, player_data in self._players.items():
            number = player_data['number']
            if number > winner_number:
                winner = player_id
                winner_number = number
        for player_id, player_data in self._players.items():
            if winner == player_id:
                name = player_data['name']
                log(f'Player {name} is the winner!')
                won = TRUE
            else:
                won = FALSE
            stream_out = player_data['stream_out']
            stream_out.write(won)
            await stream_out.drain()

    def _new_player(self):
        self._counter += 1
        return self._counter

    async def _collect_data(self, player_id, client):
        log(f'Connection accepted', client)
        stream_in = self._players[player_id]['stream_in']
        stream_out = self._players[player_id]['stream_out']
        stream_out.write(TRUE)
        await stream_out.drain()

        client = player_id
        log(f'Waiting for player {player_id}...', client)
        data = await stream_in.read(1024)
        name = data.decode()

        client = f'{player_id} -> {name.zfill(10)}'
        log(f'Player {player_id} is called {name}', client)
        self._players[player_id]['name'] = name
        self._players[player_id]['number'] = None

        log(f'Waiting for player {name} number...', client)
        data = await stream_in.read(1024)
        number = int(data)
        self._players[player_id]['number'] = number
        self._numbers += 1
        log(f'Player {name} chose {number}', client)

    async def _deny(self, stream_in, stream_out, client):
        log(f'Connection denied', client)
        log(f'The maximum number of players already reached', client)
        stream_out.write(FALSE)
        await stream_out.drain()

        log('Closing the client socket...', client)
        stream_out.close()
        log('Client socket closed\n', client)

    async def _discover_players(self, stream_in, stream_out):
        ip, port = stream_out.get_extra_info('peername')
        client = f'{ip}:{port}'
        log(f'Connection opened', client)
        player_id = self._new_player()
        if player_id > self._max_players:
            await self._deny(stream_in, stream_out, client)
        else:
            self._players[player_id] = {
                'stream_in': stream_in, 'stream_out': stream_out}
            await self._collect_data(player_id, client)
            if self._numbers == self._max_players:
                await self.start()


Server(2)

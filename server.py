from asyncio import get_event_loop, start_server, sleep
from utils import log, SERVER_IP, SERVER_PORT, COLOUR_NAME
from protal import ServerProtal, DISCONNECT, ROOM_INFO, NAME, COLOUR, DATA
from protal import PAINT, ROW, COLUMN
from game import Orbitals, Player


class Server:
    def __init__(self):
        loop = get_event_loop()
        self._protocol = ServerProtal(COLOUR_NAME)
        self._game = None
        self._started = False
        self._room_size = None
        self._players = [None]
        self._extra_turn = []
        self._last_turn = False
        self._winner = None
        self._disconnected = 0

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

    async def _get_player_info(self, stream_in):
        stream = await stream_in.read(1024)
        event, data = self._protocol.recv(stream)

        if event != DATA:
            raise RuntimeError(
                f'Expected player info, got {hex(event)} instead')

        room_size = data.get(ROOM_INFO, None)
        name = data.get(NAME, None)
        colour = data[COLOUR]

        if room_size and self._game is None:
            self._game = Orbitals(room_size)
            self._room_size = room_size
        player = Player(name)
        self._players.append(player)
        self._game.add_player(player, colour)
        return player

    async def _discover_players(self, stream_in, stream_out):
        stream = self._protocol.allow()
        stream_out.write(stream)
        await stream_out.drain()

        if stream[1] == DISCONNECT:
            stream_out.close()
            return

        waiting = False
        player = None
        while True:
            if self._winner:
                won = False
                if player.get_id() == self._winner:
                    print('player', self._winner, 'won')
                    print('End of the game...')
                    won = True
                stream = self._protocol.request_disconnect(
                    winner=won, matrix=self._matrix)
                stream_out.write(stream)
                await stream_out.drain()
                break
            if not player:
                player = await self._get_player_info(stream_in)
                stream = self._protocol.wait()
                stream_out.write(stream)
                await stream_out.drain()
                waiting = True
                continue

            if not self._started:
                if self._room_size == len(self._players) - 1:
                    # Warning: player_order is being shuffled inside self._game
                    # fix that?
                    self._player_order, self._matrix = self._game.start()
                    self._started = True
                await sleep(0)
            elif not player.is_ready():
                if self._extra_turn:
                    playing_extra = player.get_id() in self._extra_turn
                    if playing_extra:
                        waiting = False
                        stream = self._protocol.request_paint(
                            self._extra_turn, self._matrix, player.get_id(),
                            extra_turn=playing_extra)
                    else:
                        if not waiting:
                            waiting = True
                            stream = self._protocol.wait()
                            stream_out.write(stream)
                            await stream_out.drain()
                        await sleep(0)
                        continue
                else:
                    waiting = False
                    stream = self._protocol.request_paint(
                        self._player_order, self._matrix, player.get_id())

                if waiting:
                    continue

                stream_out.write(stream)
                await stream_out.drain()

                stream = await stream_in.read(1024)
                event, data = self._protocol.recv(stream)

                if event != PAINT:
                    raise RuntimeError('Player should have sent a paint spot')

                colour = data[COLOUR]
                row = data[ROW]
                column = data[COLUMN]

                self._game.paint(player, row, column, colour)

                if self._game.is_turn_ready():
                    try:
                        self._extra_turn, self._last_turn = \
                            self._game.next_turn()
                    except RuntimeError:
                        self._last_turn = self._game.extra_turn()
                        self._extra_turn = []

                    if self._last_turn:
                        self._winner = self._game.end()
            else:
                if not waiting:
                    waiting = True
                    stream = self._protocol.wait()
                    stream_out.write(stream)
                    await stream_out.drain()
                await sleep(0)

        stream_out.close()


if __name__ == "__main__":
    Server()

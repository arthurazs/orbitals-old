from random import seed, shuffle
from utils import BLANK, RED, GREEN, BLUE
from utils import CODE_BLANK, COLOURS


class Matrix:
    def __init__(self, size):
        self._spots = size ** 2
        self._spots_painted = 0

        matrix = []
        for row in range(size):
            new_row = []
            for col in range(size):
                new_row.append(BLANK)
            matrix.append(new_row)
        self._matrix = matrix

    def get_colour(self, row, col):
        return self._matrix[row][col]

    def paint(self, row, col, colour):
        if colour != BLANK:
            self._spots_painted += 1
        else:
            self._spots_painted -= 1
        self._matrix[row][col] = colour

    def all_painted(self):
        return self._spots_painted == self._spots

    def get_coloured_matrix(matrix):
        string = ''
        for row in matrix:
            string += '|'
            for col in row:
                string += Orbitals.get_coloured_col('#', '|', col)
            string += '\n'
        return string

    def get_matrix(self):
        return self._matrix
        print('Matrix')
        for row in self._matrix:
            print('', end='|')
            for col in row:
                Orbitals.colour_print('#', '|', col)
            print()

    def colour_count(self, colours):
        colour_counter = {}
        for colour in colours:
            colour_counter[colour] = 0
        for row in self._matrix:
            for colour in row:
                if colour in colours:
                    colour_counter[colour] += 1
        return colour_counter


class Orbitals:

    def __init__(self, number_of_players, starting_seed=None):
        if starting_seed:
            seed(starting_seed)
        self._number_of_players = number_of_players
        self._matrix = Matrix(number_of_players)
        self._free_colours = [RED, GREEN, BLUE]
        self._colours_allowed = []
        self._players = [None]
        self._players_order = []
        self._started = False
        self._painting_colours = [None] * (self._number_of_players + 1)
        self._players_painting = 0
        self._extra_turn_players = []
        self._max_rounds = self._number_of_players ** 2
        self._round = 1

    def start(self):
        if len(self._players) - 1 < self._number_of_players:
            raise RuntimeError('There are players missing')
        shuffle(self._players_order)
        self._started = True
        return self._players_order, self.get_matrix()

    def end(self):
        if not self._started:
            raise RuntimeError('Game not started yet')
        if self._extra_turn_players:
            raise RuntimeError('There is an extra_turn')
        if self._round <= self._max_rounds or not self._winner():
            raise RuntimeError('Game has not finished yet')
        winner = self._winner()
        self.__init__(0)
        return winner

    def _get_player(self, player_id):
        return self._players[player_id]

    def is_turn_ready(self):
        normal = self._players_painting == self._number_of_players
        extra = self._players_painting == len(self._extra_turn_players)
        return normal or extra

    def extra_turn(self):
        if not self._started:
            raise RuntimeError('Game not started yet')
        if not self._extra_turn_players:
            raise RuntimeError('There is no extra turn this round')
        if self._players_painting < len(self._extra_turn_players):
            raise RuntimeError('Not all players have picked '
                               'a spot to paint yet')

        while self._extra_turn_players:
            player_id = self._extra_turn_players.pop(0)
            row, col, colour = self._painting_colours[player_id]
            spot_colour = self._matrix.get_colour(row, col)
            if spot_colour == colour:
                colour = BLANK
            self._matrix.paint(row, col, colour)
            self._get_player(player_id).painted()

        self._players_painting = 0
        # self._print_matrix()
        last_round = False
        if self._matrix.all_painted() or self._round > self._max_rounds:
            self._round = self._max_rounds + 1
            if self._winner():
                last_round = True
        return last_round

    def next_turn(self):
        if not self._started:
            raise RuntimeError('Game not started yet')
        if self._extra_turn_players:
            raise RuntimeError("Can't move to next turn "
                               'until extra turn has not been solved')
        if self._round > self._max_rounds and self._winner():
            raise RuntimeError('Game has finished')
        if self._players_painting < self._number_of_players:
            raise RuntimeError('Not all players have picked '
                               'a spot to paint yet')

        previous_player = None
        extra_turn_players = []
        for player_id in self._players_order:
            row, col, colour = self._painting_colours[player_id]
            print(f'player {player_id} painting {colour} [{row}, {col}]')
            spot_colour = self._matrix.get_colour(row, col)
            if spot_colour == colour:
                colour = BLANK
                if previous_player:
                    p_id, p_row, p_col = previous_player
                    if p_row == row and p_col == col:
                        extra_turn_players.append(p_id)
            self._matrix.paint(row, col, colour)
            previous_player = (player_id, row, col)
            self._get_player(player_id).painted()
        print()

        first = self._players_order.pop(0)
        self._players_order.append(first)
        self._extra_turn_players = extra_turn_players
        self._players_painting = 0
        # self._print_matrix()
        self._round += 1
        print(f'round {self._round}/{self._max_rounds}')
        last_round = False
        if self._matrix.all_painted() or self._round > self._max_rounds:
            self._round = self._max_rounds + 1
            if not extra_turn_players and self._winner():
                last_round = True
        return extra_turn_players, last_round

    def _winner(self):
        winner_colour = (0, -1)
        draw = False
        colour_count = self._matrix.colour_count(self._colours_allowed)
        for colour, count in colour_count.items():
            if count == winner_colour[1]:
                draw = True
            elif count > winner_colour[1]:
                winner_colour = (colour, count)
                draw = False
        if draw:
            return None
        for player in self._players[1:]:
            if player.get_colour() == winner_colour[0]:
                return player.get_id()
        raise RuntimeError('Player not found')

    def paint(self, player, row, col, colour):
        player_id = player.get_id()
        if self._extra_turn_players:
            if player_id not in self._extra_turn_players:
                raise ValueError('This player cannot play the extra turn')
        else:
            if self._round > self._max_rounds and self._winner():
                raise RuntimeError('Game has finished')
        if colour not in self._colours_allowed:
            raise ValueError(
                'Colour not allowed\n'
                f'Expected {self._colours_allowed}, '
                f'got {colour} instead')
        if player.is_ready():
            raise ValueError('Player already picked a colour to paint')
        player.paint(colour)
        self._painting_colours[player_id] = (row, col, colour)
        self._players_painting += 1

    def get_matrix(self):
        return self._matrix.get_matrix()

    def add_player(self, player, colour):
        if colour not in self._free_colours:
            raise ValueError('Colour already picked by other player')
        if player in self._players:
            raise ValueError('Player already registered')
        self._free_colours.remove(colour)
        self._colours_allowed.append(colour)
        player.add_colour(colour)
        self._players.append(player)
        self._players_order.append(player.get_id())

    def colour_print(text, end, colour):
        print(
            f'{COLOURS[colour]}{text}{CODE_BLANK}',
            end=end)

    def get_coloured_col(text, end, colour):
        return f'{COLOURS[colour]}{text}{CODE_BLANK}{end}'


class Player:
    _player_count = 0

    def __init__(self, name):
        Player._player_count += 1
        self._id = Player._player_count
        self._name = name
        self._colour = None
        self._colour_to_paint = None

    def paint(self, colour):
        self._colour_to_paint = colour

    def painted(self):
        self._colour_to_paint = None

    def is_ready(self):
        return True if self._colour_to_paint else False

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def add_colour(self, colour):
        self._colour = colour

    def get_info(self):
        return self.get_id(), self.get_name(), self.get_colour()

    def get_colour(self):
        return self._colour

from struct import pack, unpack

REQUEST = 0x01
RESPONSE = 0x02

DISCONNECT = 0x10
DATA = 0x11
NAME = 0x12
COLOUR = 0x13
ROOM_INFO = 0x14
ROW = 0x15
COLUMN = 0x16

WAIT = 0x20
PAINT = 0x21
PLAYER_ID = 0x22
ORDER = 0x23
MATRIX = 0x24
EXTRA_TURN = 0x2F

WINNER = 0x31
LOSER = 0x32

NEW_ROW = 0xF0
TRUE = 0xF1
FALSE = 0xFF

HEX2TYPE = {
    0x21: int
}
TYPE2HEX = {v: k for k, v in HEX2TYPE.items()}


def pack_name(name):
    name = name.encode()
    return pack('2B', NAME, len(name)) + name


def pack_colour(colour):
    return pack('3B', COLOUR, 1, colour)


def pack_spot(row, column):
    return pack('6B', ROW, 1, row, COLUMN, 1, column)


def pack_room(room_size):
    return pack('3B', ROOM_INFO, 1, room_size)


def unpack_str(value):
    return value.decode()


def unpack_int(value):
    return unpack('B', value)[0]


def unpack_bool(value):
    return True if unpack('B', value)[0] == TRUE else False


def unpack_list(value):
    return unpack('B' * len(value), value)


def unpack_list_list(value):
    row = []
    matrix = []
    while value:
        item = value[0]
        if item == NEW_ROW:
            matrix.append(row)
            row = []
        else:
            row.append(item)
        value = value[1:]
    matrix.append(row)
    return matrix


def unpack_data(data_type, data_value):
    try:
        func = HEX2FUNC[data_type]
    except KeyError:
        raise NotImplementedError(f'Cannot unpack {hex(data_type)}')
    else:
        return func(data_value)


HEX2FUNC = {
    NAME: unpack_str,
    ROOM_INFO: unpack_int,
    COLOUR: unpack_list,
    ORDER: unpack_list,
    PLAYER_ID: unpack_int,
    MATRIX: unpack_list_list,
    ROW: unpack_int,
    COLUMN: unpack_int,
    EXTRA_TURN: unpack_bool
}


class ServerProtal:
    def __init__(self, colours):
        self._started = False
        self._room_size = None
        self._players = 0
        self._free_colours = colours
        self._picked_colours = {}

    @staticmethod
    def _pack_matrix(matrix):
        size = len(matrix)
        packed_matrix = pack('2B', MATRIX, (size ** 2) + (size - 1))
        for row in matrix:
            packed_matrix += pack('B' * size, *row)
            packed_matrix += pack('B', NEW_ROW)
        return packed_matrix[:-1]

    @staticmethod
    def _pack_extra(extra_turn):
        return pack('3B', EXTRA_TURN, 1, TRUE if extra_turn else FALSE)

    def request_paint(self, order, matrix, player_id=None, extra_turn=False):
        num_of_colours = len(self._picked_colours)
        asd = pack('4B', REQUEST, PAINT, COLOUR, num_of_colours)
        asd += pack('B' * num_of_colours, *self._picked_colours.keys())
        if player_id:
            asd += pack('3B', PLAYER_ID, 1, player_id)
        asd += pack('B' * (len(order) + 2), ORDER, len(order), *order)
        asd += self._pack_matrix(matrix)
        if extra_turn:
            asd += self._pack_extra(extra_turn)
        return asd

    def request_disconnect(self, winner, matrix):
        packed_request = pack('3B', REQUEST, DISCONNECT, WINNER if winner else LOSER)
        packed_request += self._pack_matrix(matrix)
        return packed_request

    @staticmethod
    def wait():
        return pack('2B', REQUEST, WAIT)

    def allow(self):
        if self._room_size is None:
            self._players += 1
            return self.request_info(room_info=True)
        elif self._room_size > self._players:
            self._players += 1
            return self.request_info()
        return pack('2B', REQUEST, DISCONNECT)

    def request_info(self, name=True, colour=True, room_info=False):
        args = [DATA]
        if name:
            args.append(NAME)
        if room_info:
            args.append(ROOM_INFO)
        colours = b''
        if colour:
            args.append(COLOUR)
            for colour_value in self._free_colours.keys():
                colours += pack('B', colour_value)
            args.append(len(colours))
        return pack('B' * (len(args) + 1), REQUEST, *args) + colours

    def recv(self, stream):
        response, response_stream = stream[0], stream[1:]
        if response != RESPONSE:
            raise ValueError(
                f'Expected a response, received {hex(response)} instead')

        if response_stream[0] == DATA:
            all_data = {}
            response_stream = response_stream[1:]
            while response_stream:
                data_type = response_stream[0]
                data_size = response_stream[1] + 2
                packed_data = response_stream[2: data_size]
                unpacked_data = unpack_data(data_type, packed_data)
                if data_type == ROOM_INFO:
                    self._room_size = unpacked_data
                elif data_type == COLOUR:
                    unpacked_data = unpacked_data[0]
                    colour = self._free_colours.pop(unpacked_data)
                    self._picked_colours[unpacked_data] = colour
                all_data[data_type] = unpacked_data
                response_stream = response_stream[data_size:]
            return DATA, all_data
        elif response_stream[0] == PAINT:
            response_stream = response_stream[1:]
            all_data = {}
            while response_stream:
                data_type = response_stream[0]
                data_size = response_stream[1] + 2
                packed_data = response_stream[2: data_size]
                unpacked_data = unpack_data(data_type, packed_data)
                if data_type == COLOUR:
                    unpacked_data = unpacked_data[0]
                all_data[data_type] = unpacked_data
                response_stream = response_stream[data_size:]
            return PAINT, all_data

        raise NotImplementedError(f'Response type unknown')


class ClientProtal:

    def __init__(self):
        self._colour = None
        self._colours = None
        self._player_id = None

    def get_id(self):
        return self._player_id

    def get_colour(self):
        return self._colour

    def get_colours(self):
        return self._colours

    def recv(self, stream):
        request, request_type = stream[0], stream[1:]
        if request != REQUEST:
            raise ValueError(
                f'Expected a request, received {hex(request)} instead')

        if request_type[0] == WAIT:
            return request_type[0], None
        elif request_type[0] == DISCONNECT:
            data = None
            if request_type[1:]:
                data = {
                    WINNER: request_type[1] == WINNER,
                    MATRIX: unpack_list_list(request_type[4:])}
            return DISCONNECT, data
        elif request_type[0] == DATA:
            aux = request_type
            while aux:
                aux = aux[1:]
                if aux[0] == COLOUR:
                    num_of_colours = aux[1] + 2
                    self._colours = aux[2:num_of_colours]
                    aux = None
            return DATA, request_type[1:]
        elif request_type[0] == PAINT:
            all_data = {}
            request_stream = request_type[1:]
            while request_stream:
                data_type = request_stream[0]
                data_size = request_stream[1] + 2
                packed_data = request_stream[2: data_size]
                unpacked_data = unpack_data(data_type, packed_data)
                if type(unpacked_data) == tuple:
                    unpacked_data = list(unpacked_data)
                if data_type == COLOUR:
                    self._colours = unpacked_data
                elif data_type == PLAYER_ID:
                    self._player_id = unpacked_data
                else:
                    all_data[data_type] = unpacked_data
                request_stream = request_stream[data_size:]
            return PAINT, all_data
        raise NotImplementedError(f'Request type unknown')

    def pack_info(self, name=None, colour=None, room_size=None):
        args = b''
        if name is not None:
            args += pack_name(name)
        if colour is not None:
            args += pack_colour(colour)
            self._colour = colour
        if room_size is not None:
            args += pack_room(room_size)
        return pack('2B', RESPONSE, DATA) + args

    @staticmethod
    def pack_painting(colour, row, column):
        data = pack_colour(colour) + pack_spot(row, column)
        return pack('2B', RESPONSE, PAINT) + data

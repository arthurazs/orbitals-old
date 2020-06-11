from datetime import datetime
from struct import pack

SERVER_IP = '127.0.0.1'
SERVER_PORT = 23456

TRUE = pack('?', True)
FALSE = pack('?', False)


def get_time():
    date_time = datetime.now()
    milliseconds, microseconds = str(date_time.microsecond / 1000).split('.')
    milliseconds = milliseconds.zfill(3)
    microseconds = microseconds.ljust(3, '0')
    time = date_time.strftime('%d/%m/%Y %H:%M:%S')
    return f'{time} {milliseconds}.{microseconds}ms'


def log(message, part=None, new_line=False):
    logging = ''
    if new_line:
        logging += '\n'
    if part:
        logging += f'[{part}] '
    logging += f'{get_time()} > {message}'
    print(logging)


def input_log(message, part=None, new_line=False):
    logging = ''
    if new_line:
        logging += '\n'
    if part:
        logging += f'[{part}] '
    logging += f'{get_time()} > {message}'
    return input(logging)


CODE_BLANK, BLANK = '\033[0;0m', 0
CODE_RED, RED = '\033[1;31m', 1
CODE_GREEN, GREEN = '\033[1;32m', 2
CODE_BLUE, BLUE = '\033[1;34m', 3
CODE_WHITE, WHITE = '\033[1;37m', 4
COLOURS = [CODE_BLANK, CODE_RED, CODE_GREEN, CODE_BLUE, CODE_WHITE]
COLOUR_NAME = {
    RED: 'red',
    GREEN: 'green',
    BLUE: 'blue',
    WHITE: 'white'
}

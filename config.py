# all common settings

from colorama import Fore, Back, Style, init

MIN_ROWS = 20
MIN_COLS = 30

BOTTOM_GUTTER = 7
RIGHT_GUTTER = 5
TOP_GUTTER = 1

WINHEIGHT = -1
WINWIDTH = -1

MAXLEN_PADDLE = 100
MINLEN_PADDLE = 10

FRAME_TIME = 0.1

BG_COLOR = Back.BLACK
BG_ACC_COLOR = Back.LIGHTMAGENTA_EX

BG_STAR_PROB = 0.2
MAXVEL_BALL = 10

BLOCK_X_SIZE = 2
BLOCK_Y_SIZE = 10
BLOCK_PROB = 0.75
BLOCK_COLORS = [Back.WHITE, Back.RED, Back.YELLOW, Back.GREEN]

POWERUP_PROB = 0.5
POWERUP_LIST = ['ep', 'sp', 'fb', 'bm', 'tb', 'pg']
POWERUP_DICT = {
    'ep': 'expand paddle',
    'sp': 'shrink paddle',
    'fb': 'fast ball',
    'bm': 'ball multiplier',
    'tb': 'thru-ball',
    'pg': 'paddle-grab'
}
POWERUP_X_SIZE = 1
POWERUP_Y_SIZE = 4

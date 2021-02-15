import os
import numpy as np
from colorama import init, Fore, Back, Style
import time

import config as conf
from game import Game

# clear window
os.system('clear')
init()

# check if terminal is big wnough
winRows, winCols = os.popen('stty size', 'r').read().split()
print('terminal dimensions: ' + str(winRows) + ' x ' + str(winCols))
if (int(winRows) < conf.MIN_ROWS or int(winCols) < conf.MIN_COLS):
    print('please ensure that the terminal is at least' +
          str(conf.MIN_ROWS) + ' x ' + str(conf.MIN_COLS))
    exit()

# game initialize
game = Game()
game.play()

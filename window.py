import numpy as np
import config as conf
from colorama import Fore, Back, Style, init
import random


class Window:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.ctr = 0

        self.grid = np.array(
            [[' ' for j in range(self.width)] for i in range(self.height)], dtype='object')

    def draw(self, obj):
        '''drawing on window'''
        pos, size, shape = obj.show()

        x1 = int(pos[0])
        x2 = int(pos[0] + size[0])
        y1 = int(pos[1])
        y2 = int(pos[1] + size[1])

        self.grid[x1:x2, y1:y2] = shape[:][:]

    def showFrame(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.grid[i][j], end='')
            print('')
        self.printGutter()

    def printGutter(self):
        for i in range(conf.BOTTOM_GUTTER - 1):
            print(i)
        print(self.ctr)
        self.ctr += 1


    def clearFrame(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = ' '

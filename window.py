import numpy as np
import config as conf
from colorama import Fore, Back, Style, init
import random
import os


class Window:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.ctr = 0
        self.topFrame = np.array([ Back.BLUE + ' ' + Back.RESET for i in range(width + 2)])
        self.bottomFrame = self.topFrame

        self.grid = np.array(
            [[' ' for j in range(self.width)] for i in range(self.height)], dtype='object')
        self.grid2 = self.grid

    def draw(self, obj):
        '''drawing on window'''
        pos, size, shape = obj.show()

        x1 = int(pos[0])
        x2 = int(pos[0] + size[0])
        y1 = int(pos[1])
        y2 = int(pos[1] + size[1])

        self.grid[x1:x2, y1:y2] = shape[:][:]

    def showFrame(self, numLives):
        print("\033[0;0H") #resets cursor position
        self.printTopGutter()
        for i in range(self.height):
            print(Back.BLUE + ' ' + Back.RESET, end='')
            for j in range(self.width):
                print( '\033[1m' + self.grid[i][j], end='')
            print(Back.BLUE + ' ' + Back.RESET)
        self.printBottomGutter(numLives)

    def printBottomGutter(self, numLives):
        for i in self.bottomFrame:
            print(i, end='')
        print('')
        print('Lives: ' + "\u2764\ufe0f " * numLives )
        self.ctr += 1

    def printTopGutter(self):
        for i in self.topFrame:
            print(i, end='')
        print('')


    def clearFrame(self):
        '''clears grid'''
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = ' '
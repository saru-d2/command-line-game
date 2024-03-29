import numpy as np
import config as conf
from colorama import Fore, Back, Style, init
import random
import os
import time


class Window:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.ctr = 0
        self.topFrame = np.array(
            [Back.BLUE + ' ' + Back.RESET for i in range(width + 2)])
        self.bottomFrame = self.topFrame

        self.grid = np.array(
            [[' ' for j in range(self.width)] for i in range(self.height)],
            dtype='object',
        )
        self.grid2 = self.grid.copy()
        self.startTime = time.monotonic()

    def draw(self, obj):
        '''drawing on window'''
        pos, size, shape = obj.show()

        x1 = int(pos[0])
        x2 = int(pos[0] + size[0])
        y1 = int(pos[1])
        y2 = int(pos[1] + size[1])

        self.grid[x1:x2, y1:y2] = shape[:][:]

    def showFrame(self, numLives, lenBalls, activePowerups, score, lastBrickFall, ufoLives):
        print('\033[0;0H')  # resets cursor position
        self.printTopGutter(ufoLives)
        for i in range(self.height):
            print(Back.BLUE + ' ' + Back.RESET, end='')
            for j in range(self.width):
                print('\033[1m' + self.grid[i][j], end='')
            print(Back.BLUE + ' ' + Back.RESET)
        self.printBottomGutter(numLives, lenBalls, activePowerups, score, lastBrickFall)

    def printBottomGutter(self, numLives, lenBalls, activePowerups, score, lastBrickFall):
        for i in self.bottomFrame:
            print(i, end='')
        print('')
        print('\033[0K', end='')
        print('\r Lives: ' + '\u2764\ufe0f ' * numLives + 'lenBalls: ' +
              str(lenBalls) + ' score: ' + str(score) + '  powerups: ',
              end='')
        for powerup in activePowerups:
            print(powerup['power'] + ':' + str(10 - int(time.monotonic() - powerup['time'])) + ', ', end='')
        print('time_fall: ' + str(10 - int(time.monotonic() - lastBrickFall)))
        print('')
        self.ctr += 1

    def printTopGutter(self, ufoLives):
        for i in self.topFrame:
            print(i, end='')
        print('')
        if ufoLives > -1:
            print('\033[0;0H')
            print(Back.BLUE + Fore.GREEN + '   ufo lives: ' + '\u2764\ufe0f ' * ufoLives + Fore.RESET + Back.RESET)

    def clearFrame(self):
        '''clears grid'''
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = ' '

    def getAssests(self, path):
        arr = []
        try:
            with open(path, 'r') as fd:
                for line in fd:
                    arr.append(list(line.strip('\n')))
                npArr = np.array(arr)
                return npArr
        except Exception:
            return None

    def gameOver(self, won, score):

        # print('\033[2J')
        print('\033[0K')  # set cursor to 0,0

        if won:
            art = self.getAssests('./assets/winScreen.txt')
            if art is not None:
                for i in range(art.shape[0]):
                    for j in range(art.shape[1]):
                        print(art[i][j], end='')
                    print('')

        elif not won:
            art = self.getAssests('./assets/loseScreen.txt')
            print(art.shape)
            if art is not None:
                for i in range(art.shape[0]):
                    for j in range(art.shape[1]):
                        print(art[i][j], end='')
                    print('')

        print('score: ' + str(score))
        print('time: ' + str(int(time.monotonic() - self.startTime)))

    def printWelcome(self):
        art = self.getAssests('./assets/welcome.txt')
        if art is not None:
            for i in range(art.shape[0]):
                for j in range(art.shape[1]):
                    print(art[i][j], end='')
                print('')
        time.sleep(1)

    def flash(self, level):
        self.clearFrame()
        print('\033[0;0H')
        self.printTopGutter(-1)
        for i in range(self.height):
            print(Back.BLUE + ' ' + Back.RESET, end='')
            for j in range(self.width):
                print('\033[1m' + self.grid[i][j], end='')
            print(Back.BLUE + ' ' + Back.RESET)  # resets cursor position
        print('\033[0;0H')
        print('')
        print('')
        print('\t\tONTO LEVEL ' + str(level))
        time.sleep(1)

import numpy as np
import config as conf
from colorama import Fore, Back, Style


class Paddle():
    ''' the player controlled paddle'''

    def __init__(self, x, y, maxRows, maxCols):
        self.x = int(x)
        self.y = int(y)
        self.length = 20
        self.center = x+1
        self.maxRows = maxRows
        self.maxCols = maxCols
        self.vel = 5

    def grow(self):
        '''grows the paddle'''
        if self.length < conf.MAXLEN_PADDLE:
            if self.y > 0:
                self.y -= 1
            if (self.y + self.length >= int(self.maxCols - 1)):
                self.y -= 1
            self.length += 2

    def shrink(self):
        '''grows the paddle'''
        if self.length > conf.MINLEN_PADDLE:
            self.length -= 2
            self.y += 1

    def show(self):
        '''pos, dim, shape'''
        shape = np.array([])
        for i in range(self.length):
            if i == self.length//2:
                shape = np.append(shape, Back.RED+'='+Back.RESET)
            else:
                shape = np.append(shape, Back.BLUE+'='+Back.RESET)
        # shape = np.append(shape, Fore.RESET)
        return np.array([self.x, self.y]), np.array([1, self.length]), shape

    def move(self, inChar):
        if inChar == 'a' and self.y > 0:
            if self.y - self.vel > 0:
                self.y -= self.vel
            else:
                self.y = 0
        elif inChar == 'd' and self.y + self.length < int(self.maxCols):
            if self.y + self.length + self.vel < int(self.maxCols):
                self.y += self.vel
            else:
                self.y = self.maxCols - self.length


    def reset(self):
        self.length = 20
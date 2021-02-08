import numpy as np
import config as conf
from colorama import Fore, Back, Style


class Plank():
    ''' the player controlled plamk'''

    def __init__(self, x, y, maxRows, maxCols):
        self.x = int(x)
        self.y = int(y)
        self.length = 5
        self.center = x+1
        self.maxRows = maxRows
        self.maxCols = maxCols
    def grow(self):
        if self.length < conf.MAXLEN:
            if self.y > 0:
                self.y -= 1
            self.length += 2

    def show(self):
        '''pos, dim, shape'''
        shape = np.array([])
        for i in range(self.length):
            if i == self.length//2:
                shape = np.append(shape, Fore.RED+'='+Fore.RESET)
            else: 
                shape = np.append(shape, Fore.BLUE+'='+Fore.RESET)
        # shape = np.append(shape, Fore.RESET)
        return np.array([self.x, self.y]), np.array([1, self.length]), shape

    def move(self, inChar):
        if inChar == 'a' and self.y > 0:
            self.y -= 1
        elif inChar == 'd' and self.y + self.length < int(self.maxCols):
            self.y += 1
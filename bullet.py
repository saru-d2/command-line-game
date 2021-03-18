import config as conf
from colorama import Fore, Back
import numpy as np
import random
import math


class Bullet:
    def __init__(self, pos):
        self.sprite = '|'
        self.x = pos[0]
        self.y = pos[1]
        self.xVel = -1
        self.yVel = 0
        self.color = Fore.WHITE

    def update(self):
        self.x += self.xVel
        self.y += self.yVel
        if self.x <= 0:
            return True
        return False

    def show(self):
        '''pos, dim, shape'''
        return np.array([self.x, self.y]), np.array([1, 1]), np.array([[self.color + self.sprite + Fore.RESET]])

    def handleCollWithBlock(self, block):
        if self.y >= block.y and self.y <= block.y + conf.BLOCK_Y_SIZE and self.x >= block.x and self.x <= block.x + conf.BLOCK_X_SIZE:
            return True
        return False

    def handleCollsWithUfo(self, ufo):
        if self.y >= ufo.y and self.y <= ufo.y + conf.UFO_SIZE_Y and self.x >= ufo.x and self.x <= ufo.x + conf.UFO_SIZE_X:
            return True
        return False

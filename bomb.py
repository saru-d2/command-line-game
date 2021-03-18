import config as conf
from colorama import Fore, Back
import numpy as np
import random
import math

class Bomb:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.xVel = 1
        self.yVel = 0
        self.color = Fore.WHITE
        self.sprite = [['#']]

    def update(self):
        self.x += self.xVel

    def show(self):
        '''pos, dim, shape'''
        return [self.x, self.y], [1, 1], self.sprite

    def handleCollsWithPaddle(self, paddle):
        if self.x == paddle.x and self.y >= paddle.y and self.y <= paddle.y + paddle.length:
            return True
        return False

import config as conf
from colorama import Fore, Back
import numpy as np
import random


class Block:
    def __init__(self, pos):
        self.health = random.randrange(1, 4)
        self.x = pos[0]
        self.y = pos[1]

    def hit(self):
        self.health -= 1
        if self.health == 0:
            return True
        return False
        

    def show(self, text = ''):
        sprite = np.array([[ conf.BLOCK_COLORS[self.health] + str(self.health) + Back.RESET for i in range(conf.BLOCK_Y_SIZE) ] for j in range(conf.BLOCK_X_SIZE)])
        return np.array([self.x, self.y]) , np.array([conf.BLOCK_X_SIZE, conf.BLOCK_Y_SIZE]), sprite
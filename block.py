import config as conf
from colorama import Fore, Back
import numpy as np
import random

class ParentBlock:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def show(self, text = ''):
        sprite = np.array([[ conf.BLOCK_COLORS[self.health] + str(self.health) + Back.RESET for i in range(conf.BLOCK_Y_SIZE) ] for j in range(conf.BLOCK_X_SIZE)])
        return np.array([self.x, self.y]) , np.array([conf.BLOCK_X_SIZE, conf.BLOCK_Y_SIZE]), sprite

class StandardBlock(ParentBlock):
    def __init__(self, pos):
        self.health = random.randrange(1, 4)
        
        self.type = 'standard'
        super().__init__(pos)

    def hit(self):
        self.health -= 1
        if self.health == 0:
            return True
        return False
        
class UnbreakableBlock(ParentBlock):
    def __init__(self, pos):
        self.health = 0
        
        self.type = 'unbreakable'

        super().__init__(pos)

    def hit(self):
        return False #never destroys


class ExplodingBlock(ParentBlock):
    def __init__(self, pos):
        self.health = 4
        super().__init__(pos)

    def hit(self):
        return True #always destroys

            

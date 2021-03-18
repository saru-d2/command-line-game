import config as conf
from colorama import Fore, Back
import numpy as np
import random

class ParentBlock:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def fall(self):
        self.x += conf.BLOCK_X_SIZE
        if self.x + conf.BLOCK_X_SIZE >= conf.MIN_ROWS:
            return True
        return False

    def show(self, text = ''):
        sprite = np.array([[ conf.BLOCK_COLORS[self.health] + ' ' + Back.RESET for i in range(conf.BLOCK_Y_SIZE) ] for j in range(conf.BLOCK_X_SIZE)])
        return np.array([self.x, self.y]) , np.array([conf.BLOCK_X_SIZE, conf.BLOCK_Y_SIZE]), sprite

    def printSprite(self):
        print(np.array([[ conf.BLOCK_COLORS[self.health] + ' ' + Back.RESET for i in range(conf.BLOCK_Y_SIZE) ] for j in range(conf.BLOCK_X_SIZE)]))

class StandardBlock(ParentBlock):
    def __init__(self, pos, health = -1):
        self.health = random.randrange(1, 4)
        if health != -1:
            self.health = health
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

class RainbowBlock(ParentBlock):
    def __init__(self, pos):
        self.health = 5
        super().__init__(pos)

    def tick(self):
        self.health += 1
        if self.health > 7:
            self.health = 5 

    def hit(self):
        return False
        # return True #always destroys

            

if __name__ == '__main__':
    uf = UnbreakableBlock([1, 2])
    print(uf.printSprite())
import config as conf
from colorama import Fore, Back
import numpy as np
import random
import math


class Ufo:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.health = 10 
        self.size = [conf.UFO_SIZE_X, conf.UFO_SIZE_Y]
        arr = []
        try:
            with open('assets/ufo.txt', 'r') as fd:
                for line in fd:
                    arr.append(list(line.strip('\n')))
                npArr = np.array(arr)
                self.sprite = npArr

            for row in self.sprite:
                for thing in row:
                    thing = Back.GREEN + thing + Back.RESET

        except Exception as e:
            print('wha')
            print(e)
            return None
        # print(self.sprite.shape)
        # print(self.sprite)
        # print('hi')


    def update(self, paddle):
        self.y = paddle.y + paddle.length // 2 - self.size[1] // 2

    def show(self):
        '''pos, dim, shape'''
        
        return np.array([self.x, self.y]), np.array([conf.UFO_SIZE_X, conf.UFO_SIZE_Y]), self.sprite


if __name__ == '__main__':
    uf = Ufo([1, 2])
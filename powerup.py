import config as conf
from colorama import Fore, Back
import numpy as np
import random

class Powerup:
    def __init__(self, pos, power):
        self.x = pos[0]
        self.y = pos[1]
        self.xVel = 1
        self.yVel = 0
        self.power = power
        self.sprite = np.array([[ Back.MAGENTA + ' ' + Back.RESET for i in range(conf.POWERUP_Y_SIZE)] for i in range(conf.POWERUP_X_SIZE)])
        self.sprite[0][1] = Back.MAGENTA + self.power[0] + Back.RESET
        self.sprite[0][2] = Back.MAGENTA + self.power[1] + Back.RESET


    def update(self):
        self.x += self.xVel
        if self.x >= conf.WINHEIGHT:
            return True
        return False

    def handleCollWithFloor(self):
        if self.x >= conf.WINHEIGHT:
            return True
        return False

    def handleCollWithPaddle(self, obj):
        objPos, objSize, _ = obj.show()
        if self.x >= objPos[0] and self.x <= objPos[0] + objSize[0] and self.y >= objPos[1] and self.y <= objPos[1] + objSize[1] and self.xVel > 0:
            return True
        return False

    def show(self):
        '''pos, dim, shape'''
        return np.array([self.x, self.y]), np.array([conf.POWERUP_X_SIZE, conf.POWERUP_Y_SIZE]), self.sprite 


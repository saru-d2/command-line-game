import config as conf
from colorama import Fore, Back
import numpy as np
import random

class Powerup:
    def __init__(self, pos, power, vel = [0, 0]):
        self.x = pos[0]
        self.y = pos[1]
        self.xVel = vel[0]
        self.yVel = vel[1]
        self.power = power
        self.sprite = np.array([[ Back.MAGENTA + ' ' + Back.RESET for i in range(conf.POWERUP_Y_SIZE)] for i in range(conf.POWERUP_X_SIZE)])
        self.sprite[0][1] = Back.MAGENTA + self.power[0] + Back.RESET
        self.sprite[0][2] = Back.MAGENTA + self.power[1] + Back.RESET


    def handleCollsWithWalls(self):
        if self.yVel < 0 and self.y + self.yVel< 0:
            return True
        if self.yVel  > 0 and self.y + conf.POWERUP_Y_SIZE + self.yVel > conf.WINWIDTH:
            return True
        return False

    def update(self):
        
        self.x += self.xVel
        self.xVel += conf.POWERUP_X_ACC
        self.xVel = min(self.xVel, conf.POWERUP_MAX_XVEL)

        # y val bs
        if self.handleCollsWithWalls():
            self.yVel *= -1

        self.y += self.yVel
        if self.x >= conf.WINHEIGHT:
            return True
        
        return False

    def handleCollWithFloor(self):
        if self.x >= conf.WINHEIGHT:
            return True
        return False

    def handleCollWithPaddle(self, obj):
        objPos = [obj.x, obj.y]
        objSize = [1, obj.length]
        if self.x >= objPos[0] and self.x <= objPos[0] + objSize[0] and self.y >= objPos[1] and self.y <= objPos[1] + objSize[1] and self.xVel > 0:
            return True
        return False

    def show(self):
        '''pos, dim, shape'''
        return np.array([self.x, self.y]), np.array([conf.POWERUP_X_SIZE, conf.POWERUP_Y_SIZE]), self.sprite 


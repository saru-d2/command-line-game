import config as conf
from colorama import Fore
import numpy as np
import random

class Ball:
    def __init__(self, pos, maxRows, maxCols):
        self.sprite = Fore.WHITE + '*' + Fore.RESET
        self.x = pos[0]
        self.y = pos[0]
        vel = np.array([ -1, random.randrange(-4, 4)])
        self.xVel = vel[0]
        self.yVel = vel[1]
        self.color = Fore.YELLOW
        self.maxRows = maxRows
        self.maxCols = maxCols


    def update(self):
        '''updates position'''
        self.x += self.xVel
        self.y += self.yVel
    
    def handleCollsWithWalls(self):
        if self.x <= 0 and self.xVel < 0: 
            self.xVel = self.xVel * -1
        if self.x >= self.maxRows and self.xVel > 0: 
            self.xVel = self.xVel * -1
        if self.y <=0 and self.yVel < 0:
            self.yVel = self.yVel * -1
        if self.y >= self.maxCols and self.yVel > 0:
            self.yVel = self.yVel * -1

        #check out of bounds
        if self.x < 0:
            self.x = 0
        if self.x > self.maxRows:
            self.x = self.maxRows
        if self.y < 0:
            self.y = 0
        if self.y > self.maxCols:
            self.y = self.maxCols

    def handleCollsWithPaddle(self, obj):
        objPos, objSize, _ = obj.show()
        if self.x >= objPos[0] and self.x <= objPos[0] + objSize[0] and self.y >= objPos[1] and self.y <= objPos[1] + objSize[1] and self.xVel > 0:
            self.xVel = -self.xVel
            #get dist from center of paddle
            pdlCntY = objPos[1] + (objSize[1] / 2)
            self.yVel += (self.y - pdlCntY) // 5



    def show(self):
        '''pos, dim, shape'''
        return np.array([self.x, self.y]), np.array([1, 1]), np.array([[ self.color + '*' + Fore.RESET ]])

    

    

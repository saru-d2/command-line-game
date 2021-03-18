import config as conf
from colorama import Fore, Back
import numpy as np
import random
import math

from sounds import bounceSound

class Ball:
    def __init__(self, pos, vel, paddle, isLaunched):
        self.sprite =  '⚬' 
        self.x = pos[0]
        self.y = pos[1]
        self.xVel = vel[0]
        self.yVel = vel[1]
        self.color = Fore.WHITE
        self.maxRows = conf.WINHEIGHT
        self.maxCols = conf.WINWIDTH
        self.isLaunched = isLaunched
        self.paddle = paddle
        self.xVelNext = -1
        self.yVelNext = -1
        self.relY = self.y - (self.paddle.y) 

    def update(self):
        '''updates position'''
        self.x += self.xVel
        self.y += self.yVel

    def handleCollsWithWalls(self):
        if self.x <= 0 + self.xVel and self.xVel < 0:
            self.xVel = self.xVel * -1
            bounceSound()
            self.x = 0
        if self.x  + self.xVel >= self.maxRows and self.xVel > 0:
            self.xVel = self.xVel * -1
            return True  # death condition

        if self.y + self.yVel  <= 0 and self.yVel < 0:
            self.yVel = self.yVel * -1
            bounceSound()

        if self.y + self.yVel >= self.maxCols and self.yVel > 0:
            self.yVel = self.yVel * -1
            bounceSound()


        # check out of bounds
        if self.x < 0:
            self.x = 0
        if self.x >= self.maxRows:
            self.x = self.maxRows - 1
            return True  # death condition

        if self.y < 0:
            self.y = 0
        if self.y >= self.maxCols:
            self.y = self.maxCols -1
        
        return False

    def handleCollsWithPaddle(self, obj):
        objPos, objSize, _ = obj.show()
        if self.x + self.xVel >= objPos[0] and self.x + self.xVel<= objPos[0] + objSize[0] and self.y + self.yVel  >= objPos[1] and self.y + self.yVel  <= objPos[1] + objSize[1] and self.xVel > 0:
            bounceSound()
            self.xVel = -self.xVel
            # get dist from center of paddle
            pdlCntY = objPos[1] + (objSize[1] // 2)
            # self.yVel += (self.y - pdlCntY) // 5
            self.x = obj.x - 1

            dist = abs(self.y - pdlCntY)
            if self.y > pdlCntY:
                self.yVel += dist // 3
            else:
                self.yVel -= dist // 3

    def handleGrabColl(self, obj):
        objPos, objSize, _ = obj.show()
        if self.x + self.xVel >= objPos[0] and self.x + self.xVel <= objPos[0] + objSize[0] and self.y + self.yVel  >= objPos[1] and self.y + self.yVel <= objPos[1] + objSize[1] and self.xVel > 0:
            self.xVelNext = -self.xVel
            # get dist from center of paddle
            pdlCntY = objPos[1] + (objSize[1] / 2)
            self.yVelNext = self.yVel + (self.y - pdlCntY) // 5
            self.xVel = 0
            self.yVel = 0
            self.isLaunched = False
            self.x = obj.x - 1
            self.relY = self.y - self.paddle.y
            return True
        return False

    def handleCollsWithBlock(self, block):
        if self.x + self.xVel >= block.x and self.x + self.xVel <= block.x + conf.BLOCK_X_SIZE and self.y + self.yVel >= block.y and self.y + self.yVel <= block.y + conf.BLOCK_Y_SIZE:
            # hit pakka
            bounceSound()
            # if x is in range before, pakka hit on y, same vice versa
            if self.x >= block.x and self.x <= block.x + conf.BLOCK_X_SIZE:
                # hit along x
                self.yVel *= -1

            elif self.y >= block.y and self.y <= block.y + conf.BLOCK_Y_SIZE:
                # hit along y
                self.xVel *= -1

            else:
                # coming along diagonal....
                self.xVel *= -1
                self.yVel *= -1
            return True
        return False

    def destroy(self, block):
        if self.x + self.xVel >= block.x and self.x + self.xVel <= block.x + conf.BLOCK_X_SIZE and self.y + self.yVel >= block.y and self.y + self.yVel <= block.y + conf.BLOCK_Y_SIZE:
            return True
        return False

    def launch(self):
        if self.xVelNext == -1 or self.yVelNext == -1:
            vel = np.array([-1, (self.relY - self.paddle.length // 2 ) // 3])
            self.xVel = vel[0]
            self.yVel = vel[1]
        else:
            self.xVel = self.xVelNext
            self.yVel = self.yVelNext
        self.x = self.paddle.x - 1
        self.y = self.paddle.y + self.relY
        self.isLaunched = True

    def faster(self):
        if self.xVel > 0 and self.xVel < conf.MAXVEL_BALL:
            self.xVel += 1
        if self.yVel > 0 and self.yVel < conf.MAXVEL_BALL:
            self.yVel += 1
        if self.xVel < 0 and abs(self.xVel) < conf.MAXVEL_BALL:
            self.xVel -= 1
        if self.yVel < 0 and abs(self.yVel) < conf.MAXVEL_BALL:
            self.yVel -= 1

    def slower(self):
        if self.xVel > 1 and self.xVel < conf.MAXVEL_BALL:
            self.xVel -= 1
        if self.yVel > 0 and self.yVel < conf.MAXVEL_BALL:
            self.yVel -= 1
        if self.xVel < -1 and abs(self.xVel) < conf.MAXVEL_BALL:
            self.xVel += 1
        if self.yVel < 0 and abs(self.yVel) < conf.MAXVEL_BALL:
            self.yVel += 1
        

    def show(self):
        '''pos, dim, shape'''
        if self.isLaunched:
            return np.array([self.x, self.y]), np.array([1, 1]), np.array([[self.color + self.sprite + Fore.RESET]])
        return np.array([self.paddle.x - 1, self.paddle.y + self.relY]), np.array([1, 1]), np.array([[self.color + self.sprite + Fore.RESET]])

    def handleCollUfo(self, ufo):
        if self.x + self.xVel >= ufo.x and self.x + self.xVel <= ufo.x + conf.UFO_SIZE_X and self.y + self.yVel >= ufo.y and self.y + self.yVel <= ufo.y + conf.UFO_SIZE_Y:
            # hit pakka
            # if x is in range before, pakka hit on y, same vice versa
            if self.x >= ufo.x and self.x <= ufo.x + conf.UFO_SIZE_X:
                # hit along x
                self.yVel *= -1

            elif self.y >= ufo.y and self.y <= ufo.y + conf.UFO_SIZE_Y:
                # hit along y
                self.xVel *= -1

            else:
                # coming along diagonal....
                self.xVel *= -1
                self.yVel *= -1
            return True
        return False

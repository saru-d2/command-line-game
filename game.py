import os
import numpy as np
from colorama import init, Fore, Back, Style
import time
import getch
import random

from ball import Ball
import config as conf
from paddle import Paddle
from window import Window
from block import Block
from powerup import Powerup


class Game:

    # runs the game.... duh

    def __init__(self):
        print('initializing game')
        _winRows, _winCols = os.popen('stty size', 'r').read().split()
        self._winHeight = int(_winRows) - conf.BOTTOM_GUTTER
        self._winWidth = int(_winCols) - conf.RIGHT_GUTTER - 1
        conf.WINHEIGHT = self._winHeight
        conf.WINWIDTH = self._winWidth

        # initialize window, plank, ball
        self.window = Window(self._winHeight, self._winWidth)
        self.paddle = Paddle(
            self._winHeight - 2, self._winWidth/2 - 1, self._winHeight, self._winWidth)
        self.balls = []

        # making blocks
        self.blocks = []
        self.generateBlocks()

        self.numLives = 3
        self.makeBall()

        self.powerups = []

        # 0 -> just as started/ after dying, 1-> in game
        self.gameState = 0

    def makeBall(self):
        self.balls.append(Ball(np.array(
            [self.paddle.x - 1, self.paddle.y + self.paddle.length / 2]), np.array([-1, random.randrange(-4, 5)]), self.paddle, False))

    def launchBall(self):
        self.gameState = 1
        for ball in self.balls:
            ball.launch()

    def generateBlocks(self):
        for i in range(0, self._winHeight - 10, conf.BLOCK_X_SIZE):
            j = 0
            while j + conf.BLOCK_Y_SIZE < self._winWidth:
                if conf.BLOCK_PROB <= random.uniform(0, 1):
                    self.blocks.append(Block(np.array([i, j])))
                    j += conf.BLOCK_Y_SIZE
                else:
                    j += 1

    def drawObjs(self):
        self.window.draw(self.paddle)

        for block in self.blocks:
            self.window.draw(block)

        for ball in self.balls:
            self.window.draw(ball)

        for powerup in self.powerups:
            self.window.draw(powerup)

        return

    def onDying(self):
        self.gameState = 0
        self.numLives -= 1
        if self.numLives <= 0:
            self.quitGame(False)
        self.makeBall()

    def quitGame(self, won):
        '''true if won'''
        if (won):
            print('u won gg')
        else:
            print('sucker')
        raise SystemExit

    def handleInput(self):
        inChar = getch.getchar()
        if inChar == None:
            return False

        if inChar == 'q':
            # quit
            self.quitGame(won=False)

        elif inChar == ' ' and self.gameState == 0:
            self.launchBall()

        elif inChar in {'a', 'd'}:
            self.paddle.move(inChar)

        # elif inChar == 'l':
        #     self.handleBallMultiply()

    def handlePhysics(self):
        for ball in self.balls:
            ballDead = ball.handleCollsWithWalls()
            if ballDead:
                self.balls.remove(ball)
                if len(self.balls) == 0:
                    self.onDying()
            ball.handleCollsWithPaddle(self.paddle)
            self.handleCollsWithBlocks(self.blocks, ball)
            ball.update()

        for powerup in self.powerups:
            powerupActivated = powerup.handleCollWithPaddle(self.paddle)
            if powerupActivated:
                #handle powerup
                self.handlePowerup(powerup.power)
                self.powerups.remove(powerup)

            powerupDead = powerup.handleCollWithFloor()
            if powerupDead:
                self.powerups.remove(powerup)

            powerup.update()

    # def handleBallMultiply(self):
    #     balls2 = self.balls
    #     for ball in self.balls:
    #         balls2.append(Ball(np.array([ball.x, ball.y]), np.array([ball.xVel, -1 * ball.yVel]), self.paddle, True ))
    #     self.balls = balls2

    def handlePowerup(self, power):
        if power == 'ep':
            self.paddle.grow()
        elif power == 'sp':
            self.paddle.shrink()
        elif power == 'fb':
            # self.handleFastBalls()
            pass
        elif power == 'bm':
            # self.handleBallMultiply()
            pass
        elif power == 'tb':
            #handle thru
            pass
        elif power == 'pg':
            #handle 
            pass            

    def generatePowerup(self, pos):
        self.powerups.append(Powerup(pos, conf.POWERUP_LIST[random.randrange(0, 6)]))

    def handleCollsWithBlocks(self, blocks, ball):
        for block in self.blocks:
            hit = ball.handleCollsWithBlock(block)
            if hit:
                ded = block.hit()
                if ded:
                    self.blocks.remove(block)
                    # chance to generate powerup
                    if random.uniform(0, 1) > conf.POWERUP_PROB:
                        #generate powerup
                        self.generatePowerup(np.array([block.x, block.y]))
                        pass

   
    def play(self):
        while True:
            currFrameStartTime = time.monotonic()

            self.handleInput()
            self.handlePhysics()

            self.window.clearFrame()
            self.drawObjs()
            self.window.showFrame(self.numLives)

            while time.monotonic() - currFrameStartTime < conf.FRAME_TIME:
                pass
        return

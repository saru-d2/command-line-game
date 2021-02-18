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
from block import StandardBlock, UnbreakableBlock, ExplodingBlock
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
        self.paddle = Paddle(self._winHeight - 2, self._winWidth / 2 - 1,
                             self._winHeight, self._winWidth)
        self.balls = []

        # making blocks
        self.numBlocks = 0
        self.blocks = []
        self.generateBlocks()

        self.numLives = 3
        self.makeBall()

        self.powerups = []

        # 0 -> just as started/ after dying, 1-> in game
        self.gameState = 0
        self.thruFlag = 0
        self.grabFlag = 0
        self.activePowerups = []
        self.blockQueue = []

    def makeBall(self):
        self.balls.append(
            Ball(
                np.array([
                    self.paddle.x - 1, self.paddle.y + self.paddle.length / 2
                ]), np.array([0, 0]), self.paddle, False))

    def launchBall(self):
        for ball in self.balls:
            if not ball.isLaunched:
                ball.launch()

    def generateBlocks(self):
        offset = (self._winWidth % conf.BLOCK_Y_SIZE) // 2
        blockMap = np.zeros(((self._winHeight - 10) // conf.BLOCK_X_SIZE, self._winWidth // conf.BLOCK_Y_SIZE))

        for i in range((self._winHeight - 10) // 2):
            if random.uniform(0, 1) <= conf.EXPLODING_PROB :
                len = random.randrange(6, 9)
                # print(self._winWidth // conf.BLOCK_Y_SIZE )
                start = random.randrange(0, ((self._winWidth)// conf.BLOCK_Y_SIZE - len ))
                print(start)
                for j in range(start, start + len):
                    self.blocks.append(ExplodingBlock(np.array([i * conf.BLOCK_X_SIZE, j * conf.BLOCK_Y_SIZE + offset])))
                    blockMap[i][j] = 1
                    self.numBlocks += 1

        for j in range((self._winWidth) // conf.BLOCK_Y_SIZE):
            if random.uniform(0, 1) <= conf.EXPLODING_PROB :
                len = random.randrange(6, 9)
                # print(self._winWidth // conf.BLOCK_Y_SIZE )
                start = random.randrange(0, ((self._winHeight - 10)// conf.BLOCK_X_SIZE - len ))
                print(start)
                for i in range(start, start + len):
                    self.blocks.append(ExplodingBlock(np.array([i * conf.BLOCK_X_SIZE, j * conf.BLOCK_Y_SIZE + offset])))
                    blockMap[i][j] = 1
                    self.numBlocks += 1
                    # print(i, j)

        i = 0
        while i + conf.BLOCK_X_SIZE < self._winHeight - 10:
            j = 0
            while j + conf.BLOCK_Y_SIZE < self._winWidth:
                if conf.BLOCK_PROB > random.uniform(0, 1) and blockMap[i // conf.BLOCK_X_SIZE][j // conf.BLOCK_Y_SIZE] == 0:
                    if conf.UNBREAKABLEBLOCK_PROB > random.uniform(0, 1):
                        self.blocks.append(UnbreakableBlock(np.array([i, j + offset])))
                    else:
                        self.blocks.append(StandardBlock(np.array([i, j + offset])))
                    j += conf.BLOCK_Y_SIZE
                    self.numBlocks += 1
                else:
                    j += conf.BLOCK_Y_SIZE
            i += conf.BLOCK_X_SIZE

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
        self.thruFlag = 0
        self.grabFlag = 0
        self.paddle.reset()
        self.powerups.clear()
        self.balls.clear()
        self.activePowerups.clear()
        self.gameState = 0
        self.numLives -= 1
        if self.numLives <= 0:
            self.quitGame(False)
        self.makeBall()

    def quitGame(self, won):
        '''true if won'''
        self.window.gameOver(won, self.numBlocks - len(self.blocks))
        raise SystemExit

    def handleInput(self):
        inChar = getch.getchar()
        if inChar == None:
            return False

        if inChar == 'q':
            # quit
            self.quitGame(won=False)

        elif inChar == ' ':
            self.launchBall()

        elif inChar in {'a', 'd'}:
            self.paddle.move(inChar)

        # elif inChar == 'l':
        #     self.grabFlag = True

        # elif inChar == 'k':
        #     self.paddle.shrink()

    def handleExploding(self):
        newQueue = []
        for block in self.blockQueue:
            if block.health == 4:
                for b in self.blocks:
                        if b == block:
                            continue
                        if abs(b.x - block.x) <= conf.BLOCK_X_SIZE and abs(b.y - block.y) <= conf.BLOCK_Y_SIZE:
                            newQueue.append(b)
            if block in self.blocks : 
                self.blocks.remove(block)
        self.blockQueue.clear()
        self.blockQueue = newQueue


    def handlePhysics(self):
        
        self.handleExploding()

        for ball in self.balls:
            ballDead = ball.handleCollsWithWalls()
            if ballDead:
                self.balls.remove(ball)
                if len(self.balls) == 0:
                    self.onDying()
            if self.grabFlag == 0:
                ball.handleCollsWithPaddle(self.paddle)
            else:
                ret = ball.handleGrabColl(self.paddle)
                if ret:
                    # self.gameState = 0
                    pass

            self.handleCollsWithBlocks(self.blocks, ball)
            ball.update()

        for powerup in self.powerups:
            powerupActivated = powerup.handleCollWithPaddle(self.paddle)
            if powerupActivated:
                # handle powerup
                self.handlePowerup(powerup.power)
                self.powerups.remove(powerup)
                if powerup.power != 'bm':
                    self.activePowerups.append({
                        'time': time.monotonic(),
                        'power': powerup.power
                    })

            powerupDead = powerup.handleCollWithFloor()
            if powerupDead:
                self.powerups.remove(powerup)
            powerup.update()

        for powerup in self.activePowerups:
            if time.monotonic() - powerup['time'] >= conf.POWERUP_EXPIRE_TIME:
                # expired
                self.resetPower(powerup['power'])
                self.activePowerups.remove(powerup)

    def resetPower(self, power):
        if power == 'ep':
            self.paddle.shrink()
        elif power == 'sp':
            self.paddle.grow()
        elif power == 'tb':
            self.thruFlag -= 1
        elif power == 'pg':
            self.grabFlag -= 1
        elif power == 'fb':
            for ball in self.balls:
                ball.slower()

    def handleBallMultiply(self):
        balls2 = self.balls.copy()
        for ball in self.balls:
            balls2.append(
                Ball(np.array([ball.x, ball.y]),
                     np.array([ball.xVel, -1 * ball.yVel]), self.paddle, True))
        self.balls = balls2

    def handleFastBalls(self):
        for ball in self.balls:
            ball.faster()

    def handlePowerup(self, power):
        if power == 'ep':
            self.paddle.grow()
        elif power == 'sp':
            self.paddle.shrink()
        elif power == 'fb':
            self.handleFastBalls()
            pass
        elif power == 'bm':
            self.handleBallMultiply()
            pass
        elif power == 'tb':
            # handle thru
            self.thruFlag += 1
            pass
        elif power == 'pg':
            self.grabFlag += 1
            # handle
            pass

    def generatePowerup(self, pos):
        self.powerups.append(
            Powerup(pos, conf.POWERUP_LIST[random.randrange(0, 6)]))

    def handleCollsWithBlocks(self, blocks, ball):
        # if self.thruFlag == 0:
        for block in self.blocks:
            if self.thruFlag == 0:
                hit = ball.handleCollsWithBlock(block)
            else:
                hit = ball.destroy(block)
            if hit:
                ded = block.hit()
                if ded or self.thruFlag > 0:
                    if block.health == 4: #exploding
                        for b in self.blocks:
                            if b == block:
                                continue
                            if abs(b.x - block.x) <= conf.BLOCK_X_SIZE and abs(b.y - block.y) <= conf.BLOCK_Y_SIZE:
                                self.blockQueue.append(b)
                    if block in self.blocks:
                        self.blocks.remove(block)
                    # chance to generate powerup
                    if random.uniform(0, 1) > conf.POWERUP_PROB:
                        # generate powerup
                        self.generatePowerup(np.array([block.x, block.y]))
                        pass
        
    def checkWinningCondition(self):
        for block in self.blocks:
            if block.health != 0:
                return False
        self.quitGame(True)
        return True

    def play(self):
        self.window.printWelcome()
        while True:
            currFrameStartTime = time.monotonic()

            self.handleInput()
            self.handlePhysics()

            self.checkWinningCondition()
            self.window.clearFrame()
            self.drawObjs()
            self.window.showFrame(self.numLives, len(self.balls),
                                  self.activePowerups, self.numBlocks - len(self.blocks))

            while time.monotonic() - currFrameStartTime < conf.FRAME_TIME:
                pass
        return

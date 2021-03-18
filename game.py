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
from block import StandardBlock, UnbreakableBlock, ExplodingBlock, RainbowBlock
from powerup import Powerup
from generateLevel import generateLevel
from bullet import Bullet
from ufo import Ufo
from bomb import Bomb


class Game:

    # runs the game.... duh

    def __init__(self):
        print('initializing game')
        _winRows, _winCols = os.popen('stty size', 'r').read().split()
        self._winHeight = conf.MIN_ROWS
        self._winWidth = conf.MIN_COLS
        conf.WINHEIGHT = self._winHeight
        conf.WINWIDTH = self._winWidth
        self.score = 0

        # initialize window, plank, ball
        self.window = Window(self._winHeight, self._winWidth)
        self.paddle = Paddle(self._winHeight - 2, self._winWidth / 2 - 1,
                             self._winHeight, self._winWidth)

        self.level = 1
        self.numBlocks = 0
        # self.blocks = []
        # self.generateBlocks()
        self.blocks = generateLevel(1)

        self.balls = []
        self.numLives = 5
        self.ufoLives = -1
        self.makeBall()

        self.shootFlag = 0
        self.powerups = []

        self.bullets = []

        # 0 -> just as started/ after dying, 1-> in game
        self.gameState = 0
        self.thruFlag = 0
        self.grabFlag = 0
        self.explodeFlag = 0
        self.activePowerups = []
        self.blockQueue = []
        self.brickLastFallTime = time.monotonic()
        self.ufo = None
        self.bombs = []
        self.ufoTimer = time.monotonic()

    def makeBall(self):
        self.balls.append(
            Ball(
                np.array([
                    self.paddle.x - 1, self.paddle.y +
                    random.randrange(0, self.paddle.length)
                ]), np.array([0, 0]), self.paddle, False))

    def launchBall(self):
        for ball in self.balls:
            if not ball.isLaunched:
                ball.launch()

    def drawObjs(self):
        self.window.draw(self.paddle)
        
        for block in self.blocks:
            self.window.draw(block)
        for ball in self.balls:
            self.window.draw(ball)
        for powerup in self.powerups:
            self.window.draw(powerup)
        for bullet in self.bullets:
            self.window.draw(bullet)
        if self.ufo is not None:
            self.window.draw(self.ufo)
        for bomb in self.bombs:
            self.window.draw(bomb)
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

    def skipLevel(self):
        self.blocks.clear()

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

        elif inChar == 'p':
            self.skipLevel()

        elif inChar == 'l':
            self.shootFlag = 1

    def handleExploding(self):
        newQueue = []
        for block in self.blockQueue:
            if block.health == 4:
                for b in self.blocks:
                    if b == block:
                        continue
                    if abs(b.x - block.x) <= conf.BLOCK_X_SIZE and abs(
                            b.y - block.y) <= conf.BLOCK_Y_SIZE:
                        newQueue.append(b)
            if block in self.blocks:
                self.blocks.remove(block)
                self.score += 1
        self.blockQueue.clear()
        self.blockQueue = newQueue

    def spawnBricks(self, x):
        y = 0
        offset = (conf.MIN_COLS % conf.BLOCK_Y_SIZE) // 2
        while y  < 9:
            self.blocks.append(StandardBlock(np.array([x*conf.BLOCK_X_SIZE, y * conf.BLOCK_Y_SIZE + offset])))
            # i+=conf.BLOCK_Y_SIZE
            y += 1

    def ufoHit(self):
        self.ufoLives -= 1
        if self.ufoLives == 3:
            self.spawnBricks(4)
        if self.ufoLives == 1:
            self.spawnBricks(5)
            

    def handleCollsBallUfo(self, ball):
        hit = ball.handleCollUfo(self.ufo)

        if hit:
            self.ufoHit()

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

        for block in self.blocks:
            if block.health >= 5:
                block.tick()

        for bullet in self.bullets:
            ded = bullet.update()
            if ded and bullet in self.bullets:
                self.bullets.remove(bullet)

        for bullet in self.bullets:
            self.handleCollsWithBlocksAndBullets(bullet)

        if self.shootFlag > 0:
            # shooootttt
            self.bullets.append(
                Bullet(np.array([self.paddle.x, self.paddle.y])))
            self.bullets.append(
                Bullet(np.array([self.paddle.x, self.paddle.y + self.paddle.length])))


        

        if self.ufo is not None:
            self.ufo.update(self.paddle)
            if time.monotonic() - self.ufoTimer > conf.UFO_BOMB_INTERVAL:
                self.bombs.append(Bomb([self.ufo.x + 4, self.ufo.y + 8]))
                self.ufoTimer = time.monotonic()

            for bullet in self.bullets:
                if bullet.handleCollsWithUfo(self.ufo):
                    # self.ufoLives -= 1
                    self.ufoHit()
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

            for ball in self.balls:
                self.handleCollsBallUfo(ball)

            for bomb in self.bombs:
                hit = bomb.handleCollsWithPaddle(self.paddle)
                if hit:
                    self.numLives -= 1
                    if bomb in self.bombs:
                        self.bombs.remove(bomb)

            for bomb in self.bombs:
                bomb.update()


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
        elif power == 'sh':
            self.shootFlag -= 1
        elif power == 'eb':
            self.explodeFlag -= 1

    def handleBallMultiply(self):
        balls2 = self.balls.copy()
        for ball in self.balls:
            balls2.append(
                Ball(np.array([ball.x, ball.y]),
                     np.array([ball.xVel, -1 * ball.yVel]), self.paddle,
                     ball.isLaunched))
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
        elif power == 'sh':
            self.shootFlag += 1

        elif power == 'eb':
            self.explodeFlag += 1

    def generatePowerup(self, pos, vel):
        if self.level < 3:
            self.powerups.append(
                Powerup(pos, conf.POWERUP_LIST[7], vel))

    def handleCollsWithBlocks(self, blocks, ball):
        # if self.thruFlag == 0:
        initVelx = ball.xVel
        initVely = ball.yVel
        for block in self.blocks:
            if self.thruFlag == 0:
                hit = ball.handleCollsWithBlock(block)
            else:
                hit = ball.destroy(block)
            if hit:
                ded = block.hit()

                if ded or self.thruFlag > 0 or self.explodeFlag > 0:
                    if block.health == 4 or self.explodeFlag > 0:  # exploding
                        for b in self.blocks:
                            if b == block:
                                continue
                            if abs(b.x - block.x) <= conf.BLOCK_X_SIZE and abs(
                                    b.y - block.y) <= conf.BLOCK_Y_SIZE:
                                self.blockQueue.append(b)
                    if block in self.blocks:
                        self.blocks.remove(block)
                        self.score += 1
                    # chance to generate powerup
                    if random.uniform(0, 1) <= conf.POWERUP_PROB:
                        # generate powerup
                        self.generatePowerup(np.array([block.x, block.y]), [
                                             initVelx, initVely])
                        pass
                if block.health >= 5:  # rainbow
                    self.blocks.remove(block)
                    self.blocks.append(StandardBlock(
                        np.array([block.x, block.y]), block.health - 4))

    def handleCollsWithBlocksAndBullets(self, bullet):
        for block in self.blocks:
            hit = bullet.handleCollWithBlock(block)
            if hit:
                ded = block.hit()

                if ded:
                    if block.health == 4:  # exploding
                        for b in self.blocks:
                            if b == block:
                                continue
                            if abs(b.x - block.x) <= conf.BLOCK_X_SIZE and abs(
                                    b.y - block.y) <= conf.BLOCK_Y_SIZE:
                                self.blockQueue.append(b)
                
                    if block in self.blocks:
                        self.blocks.remove(block)
                        self.score += 1
                
                if block.health >= 5:  # rainbow
                    if block in self.blocks:
                        self.blocks.remove(block)
                    self.blocks.append(StandardBlock(
                        np.array([block.x, block.y]), block.health - 4))
                
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                    return

    def newLevel(self):
        self.blocks = generateLevel(self.level)
        self.thruFlag = 0
        self.grabFlag = 0
        self.paddle.reset()
        self.powerups.clear()
        self.balls.clear()
        self.makeBall()
        self.activePowerups.clear()
        self.gameState = 0
        self.shootFlag = 0
        self.bullets.clear()
        if self.level == 3:
            self.ufo = Ufo([0, self.paddle.y])
            self.ufoTimer = time.monotonic()
            self.ufoLives = 5

    def checkWinningCondition(self):
        
        if self.numLives <= 0:
            self.quitGame(False)
        
        for block in self.blocks:
            if block.health != 0 and self.level < 3:
                return False
        
        if self.ufo is not None and self.ufoLives > 0:
            return False
        
        if self.level >= 3:
            if self.ufoLives == 0:
                self.quitGame(True)

        else:
            self.level += 1
            self.window.flash(self.level)
            self.newLevel()
        return True

    def fallBricks(self):
        for brick in self.blocks:
            die = brick.fall()
            if die:
                self.quitGame(False)

    def checkBrickFall(self):
        if time.monotonic() - self.brickLastFallTime >= conf.BRICK_FALL_TIME:
            self.fallBricks()
            self.brickLastFallTime = time.monotonic()

    def play(self):
        self.window.printWelcome()
        while True:
            currFrameStartTime = time.monotonic()

            self.handleInput()
            self.handlePhysics()
            self.checkBrickFall()

            self.window.clearFrame()
            self.drawObjs()
            self.window.showFrame(self.numLives, len(self.balls),
                                  self.activePowerups,
                                  self.score, self.brickLastFallTime, self.ufoLives)

            self.checkWinningCondition()
            while time.monotonic() - currFrameStartTime < conf.FRAME_TIME:
                pass
        return

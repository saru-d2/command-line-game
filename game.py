import os
import numpy as np
from colorama import init, Fore, Back, Style
import time

import config as conf
from plank import Plank
from window import Window
import getch


class Game:

    # runs the game.... duh

    def __init__(self):
        print('initializing game')
        winRows, winCols = os.popen('stty size', 'r').read().split()
        self._winHeight = int(winRows) - conf.BOTTOM_GUTTER
        self._winWidth = int(winCols) - conf.RIGHT_GUTTER
        
        # initialize window
        self.window = Window(self._winHeight, self._winWidth)
        self.plank = Plank(int(winRows) - conf.BOTTOM_GUTTER - 2, (int(winCols) - conf.RIGHT_GUTTER)/2 - 1, self._winHeight, self._winWidth)

    def drawObjs(self):
        self.window.draw(self.plank)
        return

    def quitGame(self, won):
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

        elif inChar == ' ':
            self.plank.grow()

        elif inChar in {'a', 'd'}:
            self.plank.move(inChar)

    def play(self):
        print('starting the inf loop ON PURPOSE :O')
        while True:
            currFrameStartTime = time.monotonic()
            # self.window.printScrn()
            self.handleInput()

            self.window.clearFrame()
            self.drawObjs()
            self.window.showFrame()
            while time.monotonic() - currFrameStartTime < conf.FRAME_TIME:
                pass
        return

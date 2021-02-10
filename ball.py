import config as conf
from colorama import Fore
import numpy as np
import random

class Ball:
    def __init__(self, pos):
        self.sprite = Fore.WHITE + '*' + Fore.RESET
        self.x = pos[0]
        self.y = pos[0]
        vel = np.array([ -1, random.randrange(-4, 4)])
        self.xVel = vel[0]
        self.yVel = vel[1]
        self.color = Fore.YELLOW


    def update(self):
        '''updates position'''
        self.x += self.xVel
        self.y += self.yVel

    def show(self):
        '''pos, dim, shape'''
        return np.array([self.x, self.y]), np.array([1, 1]), np.array([[ self.color + '*' + Fore.RESET ]])

    

    

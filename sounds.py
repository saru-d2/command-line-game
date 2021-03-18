import os
import platform

def bounceSound():
    if platform.system() == 'Darwin': #mac
        os.system('afplay sounds/bounce.wav &')
    else 
        os.system('aplay -q sounds/bounce.wav&')


if __name__ == '__main__':
    bounceSound()
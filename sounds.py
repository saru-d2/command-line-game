import os

def bounceSound():
    os.system('afplay sounds/bounce.wav &')

if __name__ == '__main__':
    bounceSound()
import numpy as np
from colorama import init, Fore

length = 6
init()
shape = np.array([])
for i in range(length):
    shape = np.append(shape, Fore.BLUE+'='+Fore.RESET)
# shape = np.append(shape, Fore.RESET)
for i in range(length):
    print( shape[i], end='')

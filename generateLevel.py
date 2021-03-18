# 1 for normal, 0 for nothing, 2 for unbreakable, 3 for exploding
import config as conf
from block import StandardBlock, ExplodingBlock, UnbreakableBlock, RainbowBlock
import numpy as np
level1 = [
    [0, 1, 2, 1, 2, 1, 2, 1, 0],
    [2, 1, 3, 1, 2, 1, 3, 1, 2],
    [1, 4, 1, 3, 2, 3, 1, 4, 1],
    [3, 1, 2, 1, 3, 1, 2, 1, 3],
    [3, 0, 1, 3, 1, 3, 1, 0, 3],
    [3, 1, 3, 2, 4, 2, 3, 1, 3],
    [3, 3, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3],
    [4, 0, 4, 0, 4, 0, 4, 0, 4],
]

level2 = [
    [0, 1, 2, 1, 2, 1, 2, 1, 0],
    [2, 1, 4, 1, 2, 1, 4, 1, 2],
    [1, 1, 1, 1, 2, 1, 1, 1, 1],
    [3, 1, 2, 1, 0, 1, 2, 1, 3],
    [3, 0, 3, 3, 3, 3, 3, 0, 3],
    [3, 1, 0, 2, 4, 2, 0, 1, 3],
    [3, 0, 4, 1, 1, 1, 4, 0, 3],
    [3, 1, 0, 1, 0, 1, 0, 1, 3],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
]

level3 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 2, 0, 0],
    [2, 0, 0, 0, 2, 0, 0, 0, 2],
    [0, 2, 0, 0, 0, 0, 0, 2, 0],
]


def getCoords(x, y, offset):
    return x*conf.BLOCK_X_SIZE, y * conf.BLOCK_Y_SIZE + offset


def generateLevel(level):
    blocks = []
    offset = (conf.MIN_COLS % conf.BLOCK_Y_SIZE) // 2

    if level == 1:
        lvlArr = level1

    if level == 2:
        lvlArr = level2

    if level == 3:
        lvlArr = level3

    for i in range(9):
        for j in range(9):
            coordX, coordY = getCoords(i, j, offset)
            if lvlArr[i][j] == 0:
                continue

            elif lvlArr[i][j] == 1:
                blocks.append(StandardBlock(np.array([coordX, coordY])))

            elif lvlArr[i][j] == 2:
                blocks.append(UnbreakableBlock(np.array([coordX, coordY])))

            elif lvlArr[i][j] == 3:
                blocks.append(ExplodingBlock(np.array([coordX, coordY])))

            elif lvlArr[i][j] == 4:
                blocks.append(RainbowBlock(np.array([coordX, coordY])))

    return blocks
    # 9 rows, 9 cols

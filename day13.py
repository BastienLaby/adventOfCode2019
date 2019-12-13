# -*- coding: utf-8 -*-

import logging

from day09 import IntcodeProgram, IntcodeEndProgramSignal


tilesCharacters = {
    0: ' ',
    1: 'X',
    2: 'x',
    3: '-',
    4: 'O'
}


def solve(intcode):

    grid = {} # key = pos, value = tile type
    program = IntcodeProgram(intcode)
    # program.intcode[0] = '2'
    program.input = 0
    score = 0

    paddleAppears = False
    ballAppears = False

    while True:

        try:

            x = program.decode()
            y = program.decode()
            tile = program.decode()

            if (x, y) == (-1, 0):
                score = tile
            else:
                grid[(x, y)] = tile

            if tile == 3: # ball appears
                ballAppears = True
            if tile == 4: # paddle
                paddleAppears = True

            if ballAppears and paddleAppears:
                xpaddle, ypaddle = [(pos[0], pos[1]) for (pos, typ) in grid.items() if typ == 3][0]
                xball, yball = [(pos[0], pos[1]) for (pos, typ) in grid.items() if typ == 4][0]
                print('ball %s %s' % (xball, yball))
                print('paddle %s %s' % (xpaddle, ypaddle))
                if xpaddle < xball:
                    program.input = 1
                elif xpaddle > xball:
                    program.input = -1
                else:
                    program.input = 0
                ballAppears = False
                paddleAppears = False

        except IntcodeEndProgramSignal:

            for j in range(0, 30):
                for i in range(-50, 50):
                    print(tilesCharacters[grid.get((i, j), 0)], end=' ')
                print()
            print('score %s' % score)

            exit()

    print('Number of blocks : %s' % list(grid.values()).count(2))
    print('Score : %s' % score)


if __name__ == '__main__':

    with open(__file__.replace('.py', '.input'), 'r') as f:
        intcode = f.readline().strip().split(',')
    logging.basicConfig(level=logging.INFO)
    solve(intcode)

# -*- coding: utf-8 -*-

import logging

from day09 import IntcodeProgram, IntcodeEndProgramSignal


tilesCharacters = {
    0: ' ',
    1: 'X',
    2: 'x',
    3: '-',
    4: 'o'
}


def solve(intcode):

    grid = {} # key = pos, value = tile type
    program = IntcodeProgram(intcode)
    program.intcode[0] = '2'
    program.input = 0
    score = 0

    xball, xpaddle = None, None

    while True:

        try:

            x = program.decode()
            y = program.decode()
            tile = program.decode()

            if x == -1 and y == 0:
                score = tile
            else:
                grid[(x, y)] = tile

                if tile == 3: # paddle
                    xpaddle = x

                if tile == 4: # ball
                    xball = x

            if xpaddle and xball:
                print('xpaddle and xball detected - tiles drawn %s - block drawn %s' % (len(grid), list(grid.values()).count(2)))
                if xpaddle < xball:
                    program.input = 1
                elif xpaddle > xball:
                    program.input = -1
                else:
                    program.input = 0
                xpaddle, xball = None, None
                grid = {}

        except IntcodeEndProgramSignal:

            '''
            When do the disp^lay stop and the joystick moves ??
            '''

            # for j in range(0, 30):
            #     for i in range(-50, 50):
            #         print(tilesCharacters[grid.get((i, j), 0)], end=' ')
            #     print()

            print('IntcodeEndProgramSignal - tiles drawn %s' % len(grid))
            break


            program.adress = 0


            if not list(grid.values()).count(2):
                for j in range(0, 30):
                    for i in range(-50, 50):
                        print(tilesCharacters[grid.get((i, j), 0)], end=' ')
                    print()
                break
            print('Number of blocks : %s' % list(grid.values()).count(2))
            # grid = {}

    print('Number of blocks : %s' % list(grid.values()).count(2))
    print('Score : %s' % score)


if __name__ == '__main__':

    with open(__file__.replace('.py', '.input'), 'r') as f:
        intcode = f.readline().strip().split(',')
    logging.basicConfig(level=logging.INFO)
    solve(intcode)

# -*- coding: utf-8 -*-

import logging
import math

# import png # py -3.X -m pip install PyPNG


from day09 import IntcodeProgram, IntcodeEndProgramSignal


directionCharacter = {
    (0, 1): '^',
    (0, -1): 'v',
    (1, 0): '>',
    (-1, 0): '<',
}

colorCharacter = {
    0: '.',
    1: '#'
}


def run(intcode):

    x, y = 0, 0
    dx, dy = 0, 1
    program = IntcodeProgram(intcode, _input=0)
    grid = {}

    k = 0
    while True:
        if k > 20:
            exit()
        k += 1
        
        color = program.decode()
        print('output color %s' % color)
        grid[(x, y)] = int(color)

        turn = program.decode()
        print('output turn %s' % turn)
        dx, dy = (dy, -dx) if turn else (-dy, dx)
        x += dx
        y += dy

        # for j in range(-2, 3)[::-1]:
        #     for i in range(-2, 3):
        #         if (i, j) == (x, y):
        #             print(directionCharacter[(dx, dy)], end='')
        #         else:
        #             print(colorCharacter[grid.get((x, y), 0)], end='')
        #     print()
        # print()
        
        program.input = grid.get((x, y), 0)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    # puzzle 1

    intcode = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
         intcode = f.readlines()[0].split(',')

    # run(intcode)

    program = IntcodeProgram(intcode, _input=0)
    program.decode()
    print(program.output)
    program.decode()
    print(program.output)



# (0, 0) (0, 1)
# output color 1
# output turn 0
# (-1, 0) (-1, 0)
# output color 1
# output turn 1
# (-1, 1) (0, 1)
# output color 1
# output turn 0
# (-2, 1) (-1, 0)
# output color 1
# output turn 0
# (-2, 0) (0, -1)
# output color 1
# output turn 1
# (-3, 0) (-1, 0)
# output color 1
# output turn 0
# (-3, -1) (0, -1)
# output color 1
# output turn 1
# (-4, -1) (-1, 0)
# output color 1
# output turn 1
# (-4, 0) (0, 1)
# output color 1
# output turn 1
# (-3, 0) (1, 0)
# output color 0
# output turn 1
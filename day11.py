# -*- coding: utf-8 -*-

import logging

from day09 import IntcodeProgram, IntcodeEndProgramSignal


directionCharacters = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): '^',
    (0, -1): 'v',
}

colorCharacters = {
    0: '.',
    1: '#'
}


def solve(intcode, _input=0, printGrid=False):

    grid = {} # key = (i, j), value = value
    x, y, = 0, 0
    dx, dy = 0, -1

    program = IntcodeProgram(intcode)
    program.input = _input

    while True:

        try:
            color = program.decode()
            grid[(x, y)] = color

            turn = program.decode() # 0 : left / 1 : right
            dx, dy = (-dy, dx) if turn else (dy, -dx)
            x += dx
            y += dy

            program.input = grid.get((x, y), 0)

        except IntcodeEndProgramSignal:
            break

    print(len(grid))

    if printGrid:
        for j in range(-10, 10):
            for i in range(-50, 50):
                if (i, j) == (x, y):
                    print(directionCharacters[(dx, dy)], end=' ')
                else:
                    print(colorCharacters[grid.get((i, j), 0)], end=' ')
            print()


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # puzzle 1 answer

    intcode = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
         intcode = f.readlines()[0].split(',')

    solve(intcode, _input=0)

    # puzzle 2

    solve(intcode, _input=1, printGrid=True)

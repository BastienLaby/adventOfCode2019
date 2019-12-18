# -*- coding: utf-8 -*-

import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from day09.day09 import IntcodeProgram, IntcodeEndProgramSignal
from imglib import text_image


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
    step = 1

    while True:

        try:

            x = program.decode()
            y = program.decode()
            tile = program.decode()

            # output (-1, 0) is the score
            if x == -1 and y == 0:
                score = tile
                print('Score : %s - Blocks Lefts : %s' % (score, list(grid.values()).count(2)))

                # save the grid representation
                minX = min([i[0] for i in grid.keys()])
                maxX = max([i[0] for i in grid.keys()])
                minY = min([i[1] for i in grid.keys()])
                maxY = max([i[1] for i in grid.keys()])
                asciiImage = []
                for j in range(minY, maxY + 1):
                    rowStr = []
                    for i in range(minX, maxX + 1):
                        rowStr.append(tilesCharacters[grid[(i, j)]])
                    asciiImage.append(''.join(rowStr))
                asciiImage.append('*' * (maxX - minX + 1))
                scoreStr = 'Score : %s' % score
                asciiImage.append('*' + scoreStr.center(maxX - minX - 1) + '*')
                asciiImage.append('*' * (maxX - minX + 1))
                with open('content.txt', 'w') as f:
                    f.writelines('\n'.join(asciiImage))
                image = text_image('content.txt')
                image.save('day13/img/bricks.%.05d.png' % step)
                step += 1
    
            # else, its a game tile
            else:

                # fill the grid
                grid[(x, y)] = tile

                # save the paddle position when it appears
                if tile == 3:
                    xpaddle = x

                # when the ball appears, move the paddle depending on the two elements positions
                if tile == 4:
                    xball = x
                    if xpaddle: # in the first loop, the paddle appears after the ball
                        if xpaddle < xball:
                            program.input = 1
                        elif xpaddle > xball:
                            program.input = -1
                        else:
                            program.input = 0

        except IntcodeEndProgramSignal:
            print('End of the game !')
            break


if __name__ == '__main__':

    with open(__file__.replace('.py', '.input'), 'r') as f:
        intcode = f.readline().strip().split(',')
    logging.basicConfig(level=logging.INFO)
    solve(intcode)

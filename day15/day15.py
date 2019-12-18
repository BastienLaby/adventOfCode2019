# -*- coding: utf-8 -*-

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from day09.day09 import IntcodeProgram, IntcodeEndProgramSignal
from imglib import text_image


directionCodes = {
    (0, 1): 1,
    (0, -1): 2,
    (-1, 0): 3,
    (1, 0): 4,
}

tilesCharacters = {
    0: '#',
    1: '.',
    '?': '?',
    2: 'o',
    3 : 'O' # oxygen saturated cell
}


def explore(program, grid, x=0, y=0):
    '''
    Given a known position (x, y), explore its unknown neighbors if possible.
    '''
    for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
        
        if (x + dx, y + dy) in grid:
            continue

        program.input = directionCodes[(dx, dy)]
        output = program.decode()
        grid[(x + dx, y + dy)] = [output, (x, y)]
        if not output: # destination was a wall
            continue
        else: # destination is ok
            explore(program, grid, x + dx, y + dy)
        
        # return back
        program.input = directionCodes[(-dx, -dy)]
        program.decode()

    return grid


def printGrid(grid, filepath=''):
    minX = min([i[0] for i in grid.keys()])
    maxX = max([i[0] for i in grid.keys()])
    minY = min([i[1] for i in grid.keys()])
    maxY = max([i[1] for i in grid.keys()])
    asciiImage = []
    for j in range(minY, maxY + 1)[::-1]:
        rowStr = []
        for i in range(minX, maxX + 1):
            rowStr.append(tilesCharacters[grid.get((i, j), '?')[0]] + ' ')
        asciiImage.append(''.join(rowStr))
    if filepath:
        with open('content.txt', 'w') as f:
            f.writelines('\n'.join(asciiImage))
        image = text_image('content.txt')
        image.save(filepath)
        os.remove('content.txt')
    else:
        print('\n'.join(asciiImage))


def propagateOxygen(grid):
    
    minutes = 0
    neighbors = ((0, 1), (0, -1), (-1, 0), (1, 0))
    printGrid(grid, 'day15/img/oxygen.%.4d.png' % minutes)

    while True:
    
        # break condition = no empty cell lefts
        if not [i for i in grid if grid[i][0] == 1]:
            break

        for x, y in [i for i in grid if grid[i][0] == 2]: # loop on oxygen cells
            
            # propagate to neighbors
            for dx, dy in neighbors:
                # if the cell is empty, propagate
                if grid[(x + dx, y + dy)][0] == 1:
                    grid[(x + dx, y + dy)][0] = 2
        
            # if there is no empty neighbors, set the state of the cell to "saturated"
            if all(grid[(x + i, y + j)][0] != 1 for i, j in neighbors):
                grid[(x, y)][0] = 3

        minutes += 1
        printGrid(grid, 'day15/img/oxygen.%.4d.png' % minutes)
    
    print(minutes)


if __name__ == '__main__':

    with open(__file__.replace('.py', '.input'), 'r') as f:
        intcode = f.readline().strip().split(',')
    program = IntcodeProgram(intcode)

    # puzzle 1

    grid = {
        (0, 0) : [1, None]
    }
    explore(program, grid)

    oxygen = [i for i in grid if grid[i][0] == 2][0]
    current = oxygen
    length = 0
    while True:
        if grid[current][1] is None:
            break
        current = grid[current][1]
        length += 1
    
    print(length)

    # puzzle 2

    propagateOxygen(grid)




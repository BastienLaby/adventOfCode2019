# -*- coding: utf-8 -*-

import parse
from itertools import combinations
import copy
import math


def energy(moon):
    return (abs(moon[0]) + abs(moon[1]) + abs(moon[2])) * (abs(moon[3]) + abs(moon[4]) + abs(moon[5]))


def evolves(moons, comp):
    '''
    Evolves a component (x, y or z as 0, 1 or 2) of the system
    '''
    for a, b in combinations(moons, 2):
        if a[comp] < b[comp]:
            a[comp + 3] += 1
            b[comp + 3] -= 1
        elif a[comp] > b[comp]:
            a[comp + 3] -= 1
            b[comp + 3] += 1



def solvePuzzle1(moons, iterations):
    for t in range(iterations):
        for comp in [0, 1, 2]:
            evolves(moons, comp)
        for moon in moons:
            moon[0] += moon[3]
            moon[1] += moon[4]
            moon[2] += moon[5]
    return sum([energy(m) for m in moons])


def solvePuzzle2(moons):

    initialMoons = copy.deepcopy(moons)

    loopIndexes = [0, 0, 0] # index when each component will loop

    for comp in [0, 1 ,2]:
        it = 0
        while True:
            it += 1
            evolves(moons, comp)
            for moon in moons:
                moon[0] += moon[3]
                moon[1] += moon[4]
                moon[2] += moon[5]
            if moons == initialMoons:
                loopIndexes[comp] = it
                print('loopIndexes[%s] = %s' % (comp, it))
                break

    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)

    return lcm(lcm(loopIndexes[0], loopIndexes[1]), loopIndexes[2])

if __name__ == '__main__':

    initialMoons = []
    with open(__file__.replace('.py', '.input'), 'r') as f:
        p = parse.compile('<x={:d}, y={:d}, z={:d}>')
        for line in f.read().splitlines():
            x, y, z = p.parse(line)
            initialMoons.append([x, y, z, 0, 0, 0])

    assert solvePuzzle1([[-1, 0, 2, 0, 0, 0], [2, -10, -7, 0, 0, 0], [4, -8, 8, 0, 0, 0], [3, 5, -1, 0, 0, 0]], 10) == 179
    assert solvePuzzle1([[-8, -10, 0, 0, 0, 0], [5, 5, 10, 0, 0, 0], [2, -7, 3, 0, 0, 0], [9, -8, -3, 0, 0, 0]], 100) == 1940

    print(solvePuzzle1(copy.deepcopy(initialMoons), 1000))

    assert solvePuzzle2([[-1, 0, 2, 0, 0, 0], [2, -10, -7, 0, 0, 0], [4, -8, 8, 0, 0, 0], [3, 5, -1, 0, 0, 0]]) == 2772
    assert solvePuzzle2([[-8, -10, 0, 0, 0, 0], [5, 5, 10, 0, 0, 0], [2, -7, 3, 0, 0, 0], [9, -8, -3, 0, 0, 0]]) == 4686774924

    print(solvePuzzle2(copy.deepcopy(initialMoons)))
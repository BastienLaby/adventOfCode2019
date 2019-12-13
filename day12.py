# -*- coding: utf-8 -*-

import parse
from itertools import combinations


def energy(moon):
    return (abs(moon[0]) + abs(moon[1]) + abs(moon[2])) * (abs(moon[3]) + abs(moon[4]) + abs(moon[5]))


def evolves(moons):
    for a, b in combinations(moons, 2):
        for i in [0, 1, 2]:
            if a[i] < b[i]:
                a[i + 3] += 1
                b[i + 3] -= 1
            elif a[i] > b[i]:
                a[i + 3] -= 1
                b[i + 3] += 1
    for moon in moons:
        moon[0] += moon[3]
        moon[1] += moon[4]
        moon[2] += moon[5]


def solve(moons, iterations):
    for t in range(iterations):
        # print(t, moons)
        evolves(moons)
    return sum([energy(m) for m in moons])


if __name__ == '__main__':

    moons = []
    with open(__file__.replace('.py', '.input'), 'r') as f:
        p = parse.compile('<x={:d}, y={:d}, z={:d}>')
        for line in f.read().splitlines():
            x, y, z = p.parse(line)
            moons.append([x, y, z, 0, 0, 0])

    assert solve([[-1, 0, 2, 0, 0, 0], [2, -10, -7, 0, 0, 0], [4, -8, 8, 0, 0, 0], [3, 5, -1, 0, 0, 0]], 10) == 179
    assert solve([[-8, -10, 0, 0, 0, 0], [5, 5, 10, 0, 0, 0], [2, -7, 3, 0, 0, 0], [9, -8, -3, 0, 0, 0]], 100) == 1940

    print(solve(moons, 1000))
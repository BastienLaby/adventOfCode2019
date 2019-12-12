# -*- coding: utf-8 -*-


import math
import itertools


def norm(V):
    return math.sqrt(V[0] ** 2 + V[1] ** 2)


def normalized(V):
    return [i / norm(V) for i in V]


def getMaxAsteroidSeen(spaceMap):

    asteroids = [(i, j) for i, j in itertools.product(range(len(spaceMap)), range(len(spaceMap[0]))) if spaceMap[j][i] == '#']

    maxCount = 0
    maxI, maxJ = None, None

    for i, j in asteroids:

        directions = set()

        for i2, j2 in asteroids:

            if i == i2 and j == j2:
                continue

            direction = normalized([i2 - i, j2 - j])
            direction = [float('%.06f' % k) for k in direction]
            directions.add(tuple(direction))

        if len(directions) > maxCount:
            maxCount = len(directions)
            maxI, maxJ = i, j

    return maxCount, maxI, maxJ


if __name__ == '__main__':

    spaceMap = '.#..#\n.....\n#####\n....#\n...##'.split('\n')
    assert getMaxAsteroidSeen(spaceMap)[0] == 8
    spacemap = '......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####'.split('\n')
    assert getMaxAsteroidSeen(spacemap)[0] == 33
    spacemap = '#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.'.split('\n')
    assert getMaxAsteroidSeen(spacemap)[0] == 35
    spaceMap = '.#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..'.split('\n')
    assert getMaxAsteroidSeen(spaceMap)[0] == 41
    spaceMap = '.#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##'.split('\n')
    assert getMaxAsteroidSeen(spaceMap)[0] == 210

    with open(__file__.replace('.py', '.input'), 'r') as f:
         spaceMap = [i.strip() for i in f.readlines()]

    mostEfficientAsteroid = getMaxAsteroidSeen(spaceMap)
    print(mostEfficientAsteroid)

    Oi, Oj = mostEfficientAsteroid[1:]
    asteroids = [(i, j) for i, j in itertools.product(range(len(spaceMap)), range(len(spaceMap[0]))) if spaceMap[j][i] == '#' and not (i == Oi and j == Oj)]

    def getAngleFromVector(i, j):
        angle = math.acos(i) if j > 0 else - math.acos(i)
        angle = (angle + math.pi) % (2 * math.pi)
        angle = (angle - math.pi / 2.0) % (2 * math.pi)
        return angle

    asteroidsByAngle = {} # key = angle, value = list of directions
    for Ai, Aj in asteroids:
        D = [Ai - Oi, Aj - Oj]
        nD = normalized(D)
        angle = getAngleFromVector(nD[0], nD[1])
        angle = float('%.06f' % angle)
        asteroidsByAngle.setdefault(angle, [])
        asteroidsByAngle[angle].append((D, Ai, Aj))

    # sort asteroids of each angle by distance
    for angle, asteroidList in asteroidsByAngle.items():
        asteroidList.sort(key=lambda a: norm(a[0]))

    killCount = 0

    while killCount < 200:
        for angle in sorted(asteroidsByAngle.keys()):
            if asteroidsByAngle[angle]:
                killed = asteroidsByAngle[angle].pop(0)
                killCount += 1
                print('Kill asteroid %s (%sth)' % (killed[1:], killCount))

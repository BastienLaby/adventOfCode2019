# -*- coding: utf-8 -*-


import math
import itertools


'''
Pour chaque astéroïde
   Initialiser un set de tuples de directions
   Pour chaque autre astéroïde
      Calculer la direction normalisée
      L'ajouter au set
   Afficher somme du set
'''

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
            direction = [float('%.05f' % k) for k in direction]
            directions.add(tuple(direction))

        if len(directions) > maxCount:
            maxCount = len(directions)
            maxI, maxJ = i, j

    return maxCount, maxI, maxJ


if __name__ == '__main__':

    # assert getMaxAsteroidSeen('.#..#\n.....\n#####\n....#\n...##'.split('\n'))[0] == 8
    # assert getMaxAsteroidSeen('......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####'.split('\n'))[0] == 33
    # assert getMaxAsteroidSeen('#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.'.split('\n'))[0] == 35
    # assert getMaxAsteroidSeen('.#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..'.split('\n'))[0] == 41
    # assert getMaxAsteroidSeen('.#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##'.split('\n'))[0] == 210

    with open(__file__.replace('.py', '.input'), 'r') as f:
         spaceMap = [i.strip() for i in f.readlines()]
    mostEfficientAsteroid = getMaxAsteroidSeen(spaceMap)
    print(mostEfficientAsteroid)

    laserI, laserJ = mostEfficientAsteroid[1:]
    asteroids = [(i, j) for i, j in itertools.product(range(len(spaceMap)), range(len(spaceMap[0]))) if spaceMap[j][i] == '#' and i != laserI and j != laserJ]

    asteroidsByAngle = {} # key = angle, value = list of directions
    for i, j in asteroids:
        D = [i - laserI, j - laserJ]
        nD = normalized(D)
        angle = math.acos(nD[0]) if nD[1] > 0 else - math.acos(nD[0])
        angle -= math.pi / 2.0 # remap from [-pi, pi] to [-3pi/2, 3pi/2]
        angle = (angle + math.pi) % (2 * math.pi) # remap from [-3pi/2, 3pi/2] to [0, 2pi]
        asteroidsByAngle.setdefault(angle, [])
        asteroidsByAngle[angle].append((nD, i, j))

    for angle, asteroids in asteroidsByAngle.items():
        asteroids.sort(key=lambda a: norm(a[0]))

    # for angle in sorted(asteroidsByAngle.keys()):
    #     print(angle, asteroidsByAngle[angle])

    assert sum([len(i) for i in asteroidsByAngle.values()]) >= 200

    killedAsteroids = 0
    lastAsteroidKilled = None

    laserLoop = 1
    while True:
        print('Laser Loop %s' % laserLoop)
        breakLoop = False
        for angle in sorted(asteroidsByAngle.keys()):
            if asteroidsByAngle[angle]:
                lastAsteroidKilled = asteroidsByAngle[angle].pop(0)
                killedAsteroids += 1
                # print('Kill asteroid %s (%sth)' % (lastAsteroidKilled, killedAsteroids))
            if killedAsteroids == 200:
                breakLoop = True
                break
        if breakLoop:
            break

        laserLoop += 1

    print(lastAsteroidKilled)
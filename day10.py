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

def normalize(vec2):
    norm = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)
    vec2[0] /= norm
    vec2[1] /= norm
    return vec2

def getMaxAsteroidSeen(spaceMap):

    width = len(spaceMap)
    height = len(spaceMap[0])

    asteroids = [(i, j) for i, j in itertools.product(range(width), range(height)) if spaceMap[i][j] == '#']
    maxCount = 0

    for i, j in asteroids:

        directions = set()

        for i2, j2 in asteroids:

            if i == i2 and j == j2:
                continue

            direction = normalize([i2 - i, j2 - j])
            direction = [float('%.05f' % k) for k in direction]
            directions.add(tuple(direction))

        if len(directions) > maxCount:
            maxCount = len(directions)

    return maxCount


if __name__ == '__main__':

    assert getMaxAsteroidSeen('.#..#\n.....\n#####\n....#\n...##'.split('\n')) == 8
    assert getMaxAsteroidSeen('......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####'.split('\n')) == 33
    assert getMaxAsteroidSeen('#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###.'.split('\n')) == 35
    assert getMaxAsteroidSeen('.#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..'.split('\n')) == 41
    assert getMaxAsteroidSeen('.#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##'.split('\n')) == 210

    with open(__file__.replace('.py', '.input'), 'r') as f:
         spaceMap = [i.strip() for i in f.readlines()]
    print(getMaxAsteroidSeen(spaceMap))

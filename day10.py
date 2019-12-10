# -*- coding: utf-8 -*-


import math
import itertools

class Vector2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        norm = self.norm()
        self.x /= norm
        self.y /= norm

    @classmethod
    def dotProduct(cls, A, B):
        return A.x * B.x + A.y * B.y

    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        return False


class Asteroid(object):
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.linesOfSights = []

    def __repr__(self):
        return '(%s, %s)' % (self.i, self.j)


def getMaxVisibleAsteroids(spaceMap):

    width = len(spaceMap)
    height = len(spaceMap[0])

    asteroids = [Asteroid(i, j) for i, j in itertools.product(range(width), range(height)) if spaceMap[i][j] == '#']
    for A in asteroids:
        print(A.i, A.j)
        for B in [i for i in asteroids if i != A]:
            line = Vector2D(B.i - A.i, B.j - A.j)
            line.normalize()
            if not any(line == otherLine for otherLine in A.linesOfSights):
                print('\tadd line for %s' % B)
                A.linesOfSights.append(line)
            else:
                print('\t%s has already a similar line of sight' % B)

        print(A, len(A.linesOfSights))


if __name__ == '__main__':

    assert(Vector2D(0, 1).norm() == 1)
    assert(Vector2D(1, 1).norm() == math.sqrt(2))

    spaceMap = '.#..#\n.....\n#####\n....#\n...##'
    spaceMap = spaceMap.split('\n')

    getMaxVisibleAsteroids(spaceMap)
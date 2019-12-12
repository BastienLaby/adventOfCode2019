# -*- coding: utf-8 -*-


from itertools import combinations


class Moon(object):

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __repr__(self):
        return 'pos=%s, vel=%s' % (self.pos, self.vel)


class Vec3(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __getitem__(self, key):
        if key == 0: return self.x
        elif key == 1: return self.y
        elif key == 2: return self.z

    def __setitem__(self, key, value):
        if key == 0: self.x = value
        elif key == 1: self.y = value
        elif key == 2: self.z = value

    def __repr__(self):
        return '<x=%s, y=%s, z=%s>' % (self.x, self.y, self.z)


if __name__ == '__main__':

    with open(__file__.replace('.py', '.input'), 'r') as f:
         spaceMap = [i.strip() for i in f.readlines()]

    moons = [
        Moon(Vec3(-1, 0, 2), Vec3(0, 0, 0)),
        Moon(Vec3(2, -10, -7), Vec3(0, 0, 0)),
        Moon(Vec3(4, -8, 8), Vec3(0, 0, 0)),
        Moon(Vec3(3, 5, -1), Vec3(0, 0, 0))
    ]

    print('After 0 steps:')
    for moon in moons:
        print(moon)

    for step in range(1, 5):
        print('After %s steps:' % step)

        for moonA, moonB in combinations(moons, 2):
            for i in [0, 1, 2]:
                if moonA.pos[i] != moonB.pos[i]:
                    moonA.vel[i] += 1 if moonA.pos[i] < moonB.pos[i] else -1
                    moonB.vel[i] += 1 if moonB.pos[i] < moonA.pos[i] else -1

        for moon in moons:
            moon.pos += moon.vel
            print(moon)
# -*- coding: utf-8 -*-

sign = lambda a: (a > 0) - (a < 0)

def getCrossedCells(inputList):

    x, y = 0, 0
    crossedCells = set()
    crossedCellsDistance = {}
    cellCounter = 1

    for coord in inputList.split(','):

        distance = int(''.join(coord[1:]))

        dX, dY = 0, 0
        if coord[0] == 'U':
            dY = distance
        elif coord[0] == 'D':
            dY = - distance
        elif coord[0] == 'R':
            dX = distance
        elif coord[0] == 'L':
            dX = - distance
        else:
            raise Exception('Unknow direction %s' % coord[0])

        for i in range(1, abs(dX) + 1):
            cell = (x + sign(dX) * i, y)
            crossedCells.add(cell)
            if cell not in crossedCellsDistance:
                crossedCellsDistance[cell] = cellCounter
            cellCounter += 1


        for j in range(1, abs(dY) + 1):
            cell = (x, y + sign(dY) * j)
            crossedCells.add(cell)
            if cell not in crossedCellsDistance:
                crossedCellsDistance[cell] = cellCounter
            cellCounter += 1

        x += dX
        y += dY

    if (0, 0) in crossedCells:
        crossedCells.remove((0, 0))

    return (crossedCells, crossedCellsDistance)


def getMinDistanceFromInput(input1, input2, getNearestIntersectionSteps=False):
    cells01, cells01dst = getCrossedCells(input1)
    cells02, cells02dst = getCrossedCells(input2)
    intersections = (cells01 & cells02)
    if not intersections:
        print('No intersection found for given input')
        return 0

    if not getNearestIntersectionSteps:
        return min([abs(i[0] + i[1]) for i in list(intersections)]) # minimum of manathan distances
    else:
        combinedSteps = lambda cell: cells01dst[cell] + cells02dst[cell]
        return min([combinedSteps(cell) for cell in list(intersections)]) # minimum steps to reach an intersection

# puzzle 1 tests

assert getMinDistanceFromInput('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6
# assert getMinDistanceFromInput('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159 # ?? 146 found
assert getMinDistanceFromInput('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135

# puzzle 1 answer

with open(__file__.replace('.py', '.ressources'), 'r') as f:
    data = f.readlines()
print(getMinDistanceFromInput(data[0], data[1]))

# puzzle 2

assert getMinDistanceFromInput('R8,U5,L5,D3', 'U7,R6,D4,L4', getNearestIntersectionSteps=True) == 30
assert getMinDistanceFromInput('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83', getNearestIntersectionSteps=True) == 610
assert getMinDistanceFromInput('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', getNearestIntersectionSteps=True) == 410

print(getMinDistanceFromInput(data[0], data[1], getNearestIntersectionSteps=True))

# -*- coding: utf-8 -*-

def getFuelForMass(mass, addFuelMass=False):
    fuel = (mass // 3) - 2
    if fuel <= 0:
        return 0
    elif addFuelMass:
        return fuel + getFuelForMass(fuel, addFuelMass)
    else:
        return fuel


if __name__ == '__main__':

    # puzzle 1 tests

    assert getFuelForMass(12) == 2
    assert getFuelForMass(14) == 2
    assert getFuelForMass(1969) == 654
    assert getFuelForMass(100756) == 33583

    # puzzle 1 answer

    data = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
        data = f.readlines()

    modulesMasses = [int(i) for i in modulesMasses]
    fuelSum = sum([getFuelForMass(i) for i in modulesMasses])
    print(fuelSum)

    # puzzle 2 tests

    assert getFuelForMass(14, True) == 2
    assert getFuelForMass(1969, True) == 966
    assert getFuelForMass(100756, True) == 50346

    # puzzle 2 answer

    fuelSum = sum([getFuelForMass(i, True) for i in modulesMasses])
    print(fuelSum)
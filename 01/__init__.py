# -*- coding: utf-8 -*-

modulesMasses = [67931, 140303, 100800, 69347, 113036, 127599, 55139, 99718, 110237, 94677, 91616, 61413, 97141, 147045, 80317, 85634, 128437, 110968, 98512, 126502, 59518, 50056, 51086, 76184, 108467, 68365, 147143, 108928, 116226, 66485, 51628, 135307, 137996, 97127, 81613, 75879, 125516, 94620, 143558, 132034, 54931, 92674, 53882, 127867, 131491, 62407, 64241, 71360, 56144, 90334, 134159, 75906, 73796, 117579, 86488, 148313, 75021, 97415, 120250, 79846, 86608, 120340, 85784, 129891, 138462, 52790, 89129, 113506, 120093, 137375, 146849, 54732, 56648, 85853, 64955, 146544, 117935, 139159, 142617, 128819, 82180, 76478, 74373, 110449, 75714, 83893, 135584, 86978, 99137, 75541, 122106, 146599, 86589, 130870, 84015, 84593, 67129, 131571, 147694, 118053]

# puzzle 1

def getFuelForMass(mass):
    return (mass // 3) - 2

# puzzle 1 tests

assert getFuelForMass(12) == 2
assert getFuelForMass(14) == 2
assert getFuelForMass(1969) == 654
assert getFuelForMass(100756) == 33583

# puzzle 1 answer

fuelSum = sum([getFuelForMass(i) for i in modulesMasses])
print(fuelSum)

# puzzle 2

def getFuelForMassRecursive(mass):
    fuel = max((mass // 3) - 2, 0)
    if fuel <= 0:
        return 0
    else:
        return fuel + getFuelForMassRecursive(fuel)

# puzzle 1 tests

assert getFuelForMassRecursive(14) == 2
assert getFuelForMassRecursive(1969) == 966
assert getFuelForMassRecursive(100756) == 50346

# puzzle 2 answer

fuelSum = sum([getFuelForMassRecursive(i) for i in modulesMasses])
print(fuelSum)
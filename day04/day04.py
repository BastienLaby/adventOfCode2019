# -*- coding: utf-8 -*-


def testIncrease(password):
    return list(password) == sorted(password)


def testDoubleDigits(password):
    '''
    Must be called on a sorted list
    '''
    return max(map(password.count, password)) >= 2


if __name__ == '__main__':

    # puzzle 1 tests

    assert testIncrease('111111')
    assert testDoubleDigits('111111')

    assert not testIncrease('223450')
    assert testDoubleDigits('223450')

    assert testIncrease('123789')
    assert not testDoubleDigits('123789')

    # puzzle 1 answer

    solutions = [str(i).zfill(6) for i in range(197487, 673251 + 1)]
    solutions = list(filter(testIncrease, solutions))
    solutions = list(filter(testDoubleDigits, solutions))
    print(len(solutions))

    # puzzle 2

    def testDoubleDigits(password):
        '''
        Must be called on a sorted list
        '''
        return 2 in map(password.count, password)

    # puzzle 2 tests

    assert testDoubleDigits('112233')
    assert not testDoubleDigits('123444')
    assert testDoubleDigits('111122')

    # puzzle 2 answer

    solutions = [str(i).zfill(6) for i in range(197487, 673251 + 1)]
    solutions = list(filter(testIncrease, solutions))
    solutions = list(filter(testDoubleDigits, solutions))
    print(len(solutions))
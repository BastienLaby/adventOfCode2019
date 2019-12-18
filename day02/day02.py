# -*- coding: utf-8 -*-

import copy


def decode(instructionLIst):
    for index in range(len(instructionLIst))[::4]:
        opcode = instructionLIst[index]
        if opcode == 99:
            break
        elif opcode == 1:
            instructionLIst[instructionLIst[index + 3]] = instructionLIst[instructionLIst[index + 1]] + instructionLIst[instructionLIst[index + 2]]
        elif opcode == 2:
            instructionLIst[instructionLIst[index + 3]] = instructionLIst[instructionLIst[index + 1]] * instructionLIst[instructionLIst[index + 2]]
        else:
            assert False, "Unknow opcode %s" % opcode
    return instructionLIst


def getNounVerb(instructionLIst, match):
    for noun in range(0, 100):
        for verb in range(0, 100):
            sequence = copy.deepcopy(instructionLIst)
            sequence[1] = noun
            sequence[2] = verb
            if decode(sequence)[0] == match:
                return (noun, verb)
    return None


if __name__ == '__main__':

    # inputs

    data = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
        data = f.readlines()
    instructionList = [int(i) for i in data[0].split(',')]

    # puzzle 1 tests

    assert decode([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert decode([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert decode([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert decode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]

    # puzzle 1 answer

    sequence = copy.deepcopy(instructionList)
    sequence[1] = 12 # the "noun"
    sequence[2] = 2 # the "verb"
    print(decode(sequence)[0])

    # puzzle 2 anwser

    try:
        noun, verb = getNounVerb(instructionList, match=19690720)
        print("noun %s" % noun)
        print("verb %s" % verb)
        print(100 * noun + verb)
    except TypeError:
        print('No solution found')
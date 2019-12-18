# -*- coding: utf-8 -*-

import copy
from itertools import permutations


PARAM_COUNT = {
    1: 3, # addition - parameters = part1 | part2 | resultLocation
    2: 3, # multiplication - parameters = part1 | part2 | resultLocation
    3: 1, # input - parameter = where to write the input
    4: 1, # output - parameter = location of the thing to output
    5: 2, # jump-if-true - parameters = testValue | new pointer adress if testValue is non-zero
    6: 2, # jump-if-false - parameters = testValue | new pointer adress if testValue is zero
    7: 3, # less than - parameters = value1 | value2 | new pointer adress if value1 (or adress) < value2 (or adress)
    8: 3, # equals - parameters = value1 | value2 | new pointer adress if value1 (or adress) == value2 (or adress)
    99: 0 # end of program
}


class IntcodeEndProgramSignal(Exception):
    outputValue = None


class Amplifier(object):
    def __init__(self, intcode, phase):
        self.intcode = intcode
        self.phase = phase
        self.phaseRead = False
        self.input = None
        self.output = None
        self.adress = 0

    def decode(self):
        '''
        Decode the intcode and return the output value
        '''

        while True:

            opcode = int(self.intcode[self.adress][-2:])
            instruction = self.intcode[self.adress].zfill(2 + PARAM_COUNT[opcode]) # fill leading 0
            pModes = instruction[:-2]

            # for the following code :
            #   pX = the value of the param as it appears in the list
            #   pXValue = the value to consider when getting the param (pX if mode == 1, list[pX] if mode == 0)

            # try to get the first 3 parameters (our opcodes use a maximum of 3 parameters)
            # we can afford to get the first 3 parameters in one try, even if they not truely exists (in order to get more code lisibility)
            # we add a IndexError exception catch to detect the end of the list

            try:

                p1 = int(self.intcode[self.adress + 1]) # will not be used in opcode 99
                p2 = int(self.intcode[self.adress + 2]) # will not be used in opcodes 3, 4 and 99

                p1Value = p1 if int(pModes[-1]) else int(self.intcode[p1])
                p2Value = p2 if int(pModes[-2]) else int(self.intcode[p2])

                p3 = int(self.intcode[self.adress + 3]) # will not be used in opcodes 3, 4, 5, 6 and 99
                assert pModes[-3] == '0' # Parameters that an instruction writes to will never be in immediate mode.

            except IndexError:
                pass

            # start opcodes tests

            if opcode == 99:
                raise IntcodeEndProgramSignal()

            elif opcode == 1:
                self.intcode[p3] = str(p1Value + p2Value)
                self.adress += PARAM_COUNT[opcode] + 1

            elif opcode == 2:
                self.intcode[p3] = str(p1Value * p2Value)
                self.adress += PARAM_COUNT[opcode] + 1

            elif opcode == 3:
                if self.phaseRead:
                    self.intcode[int(self.intcode[self.adress + 1])] = self.input
                else:
                    self.intcode[int(self.intcode[self.adress + 1])] = self.phase
                    self.phaseRead = True
                self.adress += PARAM_COUNT[opcode] + 1

            elif opcode == 4:
                self.adress += PARAM_COUNT[opcode] + 1
                if p1Value:
                    self.output = p1Value
                    return

            elif opcode == 5: # jump-if-true
                self.adress = p2Value if p1Value else self.adress + PARAM_COUNT[opcode] + 1

            elif opcode == 6: # jump-if-false
                self.adress = p2Value if not p1Value else self.adress + PARAM_COUNT[opcode] + 1

            elif opcode == 7: # less-than
                self.intcode[p3] = '1' if p1Value < p2Value else '0'
                self.adress += PARAM_COUNT[opcode] + 1

            elif opcode == 8: # equals
                self.intcode[p3] = '1' if p1Value == p2Value else '0'
                self.adress += PARAM_COUNT[opcode] + 1

            else:
                raise Exception('Unknow opcode %s' % opcode)

    def printState(self):
        print('A%s ip:%s input:%s output:%s mem:%s' % (self.phase, self.adress, self.input, self.output, self.intcode))


def getAmplifierChainOutput(phaseOrder, intcode):
    amplifiers = [Amplifier(copy.deepcopy(intcode), i) for i in phaseOrder]
    output = None
    for amp in amplifiers:
        amp.input = output or 0
        amp.decode()
        output = amp.output
    return output


def getAmplifierChainLoopOutput(phaseOrder, intcode):

    amplifiers = [Amplifier(copy.deepcopy(intcode), i) for i in phaseOrder]
    output = None

    while True:
        try:
            for amp in amplifiers:
                amp.input = output or 0
                amp.decode()
                output = amp.output
        except IntcodeEndProgramSignal:
            return amp.input # we consider the amplifier A runs the ewit code, and we return the previous output code (E amplifier output)

if __name__ == '__main__':

    # puzzle 1 tests

    assert getAmplifierChainOutput([4, 3, 2, 1, 0], '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')) == 43210
    assert getAmplifierChainOutput([0, 1, 2, 3, 4], '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'.split(',')) == 54321
    assert getAmplifierChainOutput([1, 0, 4, 3, 2], '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'.split(',')) == 65210

    # puzzle 1 answer

    intcode = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
         intcode = f.readlines()[0]

    outputs = []
    for permutation in permutations([0, 1, 2, 3, 4]):
        outputs.append(getAmplifierChainOutput(permutation, intcode.split(',')))

    print(max(outputs))

    # puzzle 2 tests

    assert getAmplifierChainLoopOutput([9,8,7,6,5], '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'.split(',')) == 139629729
    assert getAmplifierChainLoopOutput([9,7,8,5,6], '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'.split(',')) == 18216

    # puzzle 2 answer

    outputs = []
    for permutation in permutations([5, 6, 7, 8, 9]):
        outputs.append(getAmplifierChainLoopOutput(permutation, intcode.split(',')))

    print(max(outputs))

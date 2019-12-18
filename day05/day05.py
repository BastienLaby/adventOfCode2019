# -*- coding: utf-8 -*-


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


def decode(instructionList, _input):

    index = 0

    while True:

        opcode = int(instructionList[index][-1])
        instruction = instructionList[index].zfill(2 + PARAM_COUNT[opcode]) # fill leading 0
        pModes = instruction[:-2]

        # for the following code :
        #   pX = the value of the param as it appears in the list
        #   pXValue = the value to consider when getting the param (pX if mode == 1, list[pX] if mode == 0)

        # try to get the first 3 parameters (our opcodes use a maximum of 3 parameters)
        # we can afford to get the first 3 parameters in one try, even if they not truely exists (in order to get more code lisibility)
        # we add a IndexError exception catch to detect the end of the list

        try:

            p1 = int(instructionList[index + 1]) # will not be used in opcode 99
            p2 = int(instructionList[index + 2]) # will not be used in opcodes 3, 4 and 99

            p1Value = p1 if int(pModes[-1]) else int(instructionList[p1])
            p2Value = p2 if int(pModes[-2]) else int(instructionList[p2])

            p3 = int(instructionList[index + 3]) # will not be used in opcodes 3, 4, 5, 6 and 99
            assert pModes[-3] == '0' # Parameters that an instruction writes to will never be in immediate mode.

        except IndexError:
            pass

        # start opcodes tests

        if opcode == 99: return

        elif opcode == 1:
            instructionList[p3] = str(p1Value + p2Value)
            index += PARAM_COUNT[opcode] + 1

        elif opcode == 2:
            instructionList[p3] = str(p1Value * p2Value)
            index += PARAM_COUNT[opcode] + 1

        elif opcode == 3:
            instructionList[int(instructionList[index + 1])] = _input
            index += PARAM_COUNT[opcode] + 1

        elif opcode == 4:
            if p1Value:
                return p1Value # should be the diagnostic code
            index += PARAM_COUNT[opcode] + 1

        elif opcode == 5: # jump-if-true
            index = p2Value if p1Value else index + PARAM_COUNT[opcode] + 1

        elif opcode == 6: # jump-if-false
            index = p2Value if not p1Value else index + PARAM_COUNT[opcode] + 1

        elif opcode == 7: # less-than
            instructionList[p3] = '1' if p1Value < p2Value else '0'
            index += PARAM_COUNT[opcode] + 1

        elif opcode == 8: # equals
            instructionList[p3] = '1' if p1Value == p2Value else '0'
            index += PARAM_COUNT[opcode] + 1


if __name__ == '__main__':

    with open(__file__.replace('.py', '.ressources'), 'r') as f:

        testList = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'.split(',')
        assert decode(testList, _input=7) == 999
        assert decode(testList, _input=8) == 1000
        assert decode(testList, _input=9) == 1001

        instructionList = f.readlines()[0].split(',')
        # diagnosticCode = decode(instructionList, _input=1)
        diagnosticCode = decode(instructionList, _input=5) # Do NOT call decode() two time on the same list. Need to copy it before.
        print(diagnosticCode)

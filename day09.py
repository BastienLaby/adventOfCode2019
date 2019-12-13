# -*- coding: utf-8 -*-

import logging


PCOUNT = {
    1: 3, # addition - parameters = part1 | part2 | resultLocation
    2: 3, # multiplication - parameters = part1 | part2 | resultLocation
    3: 1, # input - parameter = where to write the input
    4: 1, # output - parameter = location of the thing to output
    5: 2, # jump-if-true - parameters = testValue | new pointer adress if testValue is non-zero
    6: 2, # jump-if-false - parameters = testValue | new pointer adress if testValue is zero
    7: 3, # less than - parameters = value1 | value2 | new pointer adress if value1 (or adress) < value2 (or adress)
    8: 3, # equals - parameters = value1 | value2 | new pointer adress if value1 (or adress) == value2 (or adress)
    9: 1, # relative base offset
    99: 0 # end of program
}


PMODES = {
    'POSITION': '0',
    'IMMEDIATE': '1',
    'RELATIVE': '2',
}


class IntcodeEndProgramSignal(Exception):
    pass


class IntcodeParameter(object):

    def __init__(self, program, value, mode):
        assert mode in PMODES.values(), 'Unknow parameter mode %s' % mode
        self.program = program # need a reference on the intcode programm to give access to intcode and modify it
        self.value = int(value) # the value of the parameter as it appears in the intcode array
        self.mode = mode

    def getValue(self):
        '''
        Return the interpreted value based on the parameter mode
        '''
        if self.mode == PMODES['IMMEDIATE']:
            return int(self.value)
        elif self.mode == PMODES['POSITION']:
            adress = self.value
        elif self.mode == PMODES['RELATIVE']:
            adress = self.value + self.program.relativeBase
        self.program.increaseIntcodeSize(adress)
        # print(adress)
        # print(self.program.intcode[adress-2:adress+2])
        return int(self.program.intcode[adress])

    def writeValue(self, value):
        '''
        Write the given value to the parameter location (depends on the parameter mode).
        '''
        assert self.mode != PMODES['IMMEDIATE'] # Parameters that an instruction writes to will never be in immediate mode.
        if self.mode == PMODES['POSITION']:
            adress = self.value
        elif self.mode == PMODES['RELATIVE']:
            adress = self.program.relativeBase + self.value
        self.program.increaseIntcodeSize(adress)
        if value is None:
            print('value is none !!')
            exit()
        self.program.intcode[adress] = str(value)

    def __str__(self):
        return 'Parameter(m=%s, val=%s)' % (self.mode, self.getValue())

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, IntcodeParameter):
            return self.getValue() == other.getValue()
        return False

    def __lt__(self, other):
        if isinstance(other, IntcodeParameter):
            return self.getValue() < other.getValue()
        return False


class IntcodeProgram(object):
    def __init__(self, intcode, _input=None):
        self.intcode = intcode
        self.input = _input
        self.output = None
        self.adress = 0
        self.relativeBase = 0

    def increaseIntcodeSize(self, adress):
        while len(self.intcode) < adress + 1:
            self.intcode.append(0)

    def increaseAdressBy(self, adressIncrement):
        self.adress += adressIncrement
        self.increaseIntcodeSize(self.adress)

    def decode(self):
        '''
        Decode the intcode and return the output value
        '''

        while True:

            instruction = self.intcode[self.adress].zfill(2 + max(PCOUNT.values()))
            opcode = int(instruction[-2:])
            modes = instruction[:-2]
            # logging.info('instruction %s (modes %s) ip %s rel %s intcode %s' % (instruction, modes, self.adress, self.relativeBase, self.intcode[:5]))
            params = []
            for i in range(1, PCOUNT[opcode] + 1):
                params.append(IntcodeParameter(self, self.intcode[self.adress + i], modes[-i]))
            # logging.info('instruction %s (modes %s) ip %s rel %s intcode %s --> params %s' % (instruction, modes, self.adress, self.relativeBase, '[...]', params))

            # start opcodes tests

            initialAdress = self.adress

            if opcode == 99: raise IntcodeEndProgramSignal()

            elif opcode == 1: # addition
                params[2].writeValue(params[0].getValue() + params[1].getValue())

            elif opcode == 2: # multiplication
                params[2].writeValue(params[0].getValue() * params[1].getValue())

            elif opcode == 3: # write input
                params[0].writeValue(self.input)

            elif opcode == 4: # return output
                self.output = params[0].getValue()
                self.increaseAdressBy(PCOUNT[opcode] + 1)
                return self.output

            elif opcode == 5: # jump-if-true
                if params[0].getValue():
                    self.adress = params[1].getValue()

            elif opcode == 6: # jump-if-false
                if not params[0].getValue():
                    self.adress = params[1].getValue()

            elif opcode == 7: # less-than
                params[2].writeValue('1' if params[0] < params[1] else '0')

            elif opcode == 8: # equals
                params[2].writeValue('1' if params[0] == params[1] else '0')

            elif opcode == 9: # relative base offset
                self.relativeBase += params[0].getValue()
            else:
                raise Exception('Unknow opcode %s' % opcode)

            if self.adress == initialAdress:
                self.increaseAdressBy(PCOUNT[opcode] + 1)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # puzzle 1 tests

    intcode = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'.split(',')
    program = IntcodeProgram(intcode)
    for i in intcode:
        program.adress = 0
        output = program.decode()
        logging.debug(output)
        assert int(output) == int(i), 'output %s != %s' % (output, i)

    program = IntcodeProgram('1102,34915192,34915192,7,4,7,99,0'.split(','))
    assert len(str(program.decode())) == 16

    program = IntcodeProgram('104,1125899906842624,99'.split(','))
    assert program.decode() == 1125899906842624

    # # puzzle 1 answer

    intcode = None
    with open(__file__.replace('.py', '.input'), 'r') as f:
         intcode = f.readlines()[0]

    program = IntcodeProgram(intcode.split(','), _input=1)
    logging.info(program.decode())

    # puzzle 2 answer

    program = IntcodeProgram(intcode.split(','), _input=2)
    logging.info(program.decode())


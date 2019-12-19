# -*- coding: utf-8 -*-

import cProfile
from itertools import cycle, repeat, chain, compress

PATTERN = [0, 1, 0, -1]

mult = lambda i, j: i * j


def getPattern(count):
    pattern = []
    for i in PATTERN:
        pattern.extend([i] * count)
    pattern.append(pattern.pop(0))
    return pattern


def fft(signal, count=1):
    '''
    Phase the signal and return the output
    '''
    print('fft', count)
    output = []
    for index, element in enumerate(signal):
        pattern = getPattern(index + 1)
        phase = map(mult, pattern, compress(signal, cycle(pattern)))
        output.append(abs(sum(phase)) % 10)
        print('index', index, len(pattern))

    count -= 1
    if count:
        return fft(output, count)
    return output


def main():

    # puzzle 1 tests

    toStr = lambda l: ''.join([str(i) for i in l])

    assert toStr(fft([int(i) for i in '12345678'], 4)) == '01029498'
    assert toStr(fft([int(i) for i in '80871224585914546619083218645595'], 100)).startswith('24176176')
    assert toStr(fft([int(i) for i in '19617804207202209144916044189917'], 100)).startswith('73745418')
    assert toStr(fft([int(i) for i in '69317163492948606335995924319873'], 100)).startswith('52432133')

    # puzzle 1 anwser

    with open(__file__.replace('.py', '.input'), 'r') as f:
        intput = [int(i) for i in f.readline().strip()]

    signal = []
    for i in range(10000):
        signal.extend(intput)

    signal = fft(signal, 1)
    print(signal[:8])



# cProfile.run('main()')
main()
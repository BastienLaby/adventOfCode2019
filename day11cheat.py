import csv
import sys
from enum import Enum

class State(Enum):
    READY = 0
    INPUT = 1
    HALTED = 2

class Intcode:
    def load_prgm(filename):
        return [int(i) for i in list(csv.reader(open(filename)))[0]]

    def __init__(self, rom, id = "intcode"):
        self.id = id
        self.ram = rom
        self.ip = 0
        self.inputs = []
        self.outputs = []
        self.state = State.READY
        self.relbase = 0

    def add_output(self, fn):
        self.outputs.append(fn)

    def input(self, data):
        self.inputs.append(data)

    def run_instr(self):
        #Intcode.print_instr(self.ram, self.ip) # trace
        opcode = min(self.ram[self.ip] % 100, len(self.opcodes) - 1)
        self.opcodes[opcode][1](self)
        if self.ip >= len(self.ram):
            self.state = State.HALTED

    def run(self):
        while self.state != State.HALTED:
            self.run_instr()


    def tick(self):
        if self.state != State.HALTED:
            self.run_instr()

    def getmode(opcode, offset):
        return int(opcode / (10**(offset + 1))) % 10

    # pick right mode to use, return resolved addr
    def getaddr(mem, ip, opcode, offset, relbase):
        mode = Intcode.getmode(opcode, offset)
        if mode == 0: # positional
            return mem[ip + offset] if ip + offset < len(mem) else 0
        elif mode == 1: # immediate
            return ip + offset
        elif mode == 2: # relative
            addr = mem[ip + offset] if ip + offset < len(mem) else 0
            return relbase + addr

    # pick right mode to use, return resolved addr
    def getdata(mem, ip, opcode, offset, relbase):
        mode = Intcode.getmode(opcode, offset)
        addr = Intcode.getaddr(mem, ip, opcode, offset, relbase)
        return mem[addr] if addr < len(mem) else 0

    def setdata(mem, addr, value):
        if addr >= len(mem):
            mem.extend([0] * (addr + 1 - len(mem)))
        mem[addr] = value

    def running(self):
        return self.state != State.HALTED

    # opcodes start here

    # no operation: pass
    def op_nop(self):
        if self.state == State.READY:
            self.ip += 1

    # add: p3 = p1 + p2
    def op_add(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            p2 = Intcode.getdata(self.ram, self.ip, opcode, 2, self.relbase)
            p3 = Intcode.getaddr(self.ram, self.ip, opcode, 3, self.relbase)
            Intcode.setdata(self.ram, p3, p1 + p2)
            self.ip += 4

    # multiply: p3 = p1 * p2
    def op_mul(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            p2 = Intcode.getdata(self.ram, self.ip, opcode, 2, self.relbase)
            p3 = Intcode.getaddr(self.ram, self.ip, opcode, 3, self.relbase)
            Intcode.setdata(self.ram, p3, p1 * p2)
            self.ip += 4

    # input: p1 = next(input)
    def op_rcv(self):
        if len(self.inputs) == 0:
            self.state = State.INPUT
        else:
            self.state = State.READY
            opcode = self.ram[self.ip]
            p1 = Intcode.getaddr(self.ram, self.ip, opcode, 1, self.relbase)
            Intcode.setdata(self.ram, p1, self.inputs.pop(0))
            self.ip += 2

    # output: outputs.append(p1)
    def op_snd(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            for output in self.outputs:
                output(p1)
            self.ip += 2

    # branch if equal: if p1 != 0 then ip = p2
    def op_beq(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            if p1 != 0:
                p2 = Intcode.getdata(self.ram, self.ip, opcode, 2, self.relbase)
                self.ip = p2
            else:
                self.ip += 3


    # branch if not equal: if p1 == 0 then ip = p2
    def op_bne(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            if p1 == 0:
                p2 = Intcode.getdata(self.ram, self.ip, opcode, 2, self.relbase)
                self.ip = p2
            else:
                self.ip += 3

    # set if less than: if p1 < p2 then p3 = 1 else p3 = 0
    def op_slt(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            p2 = Intcode.getdata(self.ram, self.ip, opcode, 2, self.relbase)
            p3 = Intcode.getaddr(self.ram, self.ip, opcode, 3, self.relbase)
            Intcode.setdata(self.ram, p3, 1 if p1 < p2 else 0)
            self.ip += 4;

    # set if equal: if p1 == p2 then p3 = 1 else p3 = 0
    def op_seq(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            p2 = Intcode.getdata(self.ram, self.ip, opcode, 2, self.relbase)
            p3 = Intcode.getaddr(self.ram, self.ip, opcode, 3, self.relbase)
            Intcode.setdata(self.ram, p3, 1 if p1 == p2 else 0)
            self.ip += 4

    # accumulate relative base: relbase += p1
    def op_arb(self):
        if self.state == State.READY:
            opcode = self.ram[self.ip]
            p1 = Intcode.getdata(self.ram, self.ip, opcode, 1, self.relbase)
            self.relbase += p1
            self.ip += 2

    # halt: stop program
    def op_hlt(self):
        self.state = State.HALTED

    # the name of each opcode, its callback function, and the instr byte size
    opcodes = (
        ("nop", op_nop, 1), #  0  - no operation
        ("add", op_add, 4), #  1  - add
        ("mul", op_mul, 4), #  2  - multiply
        ("rcv", op_rcv, 2), #  3  - recieve
        ("snd", op_snd, 2), #  4  - send
        ("beq", op_beq, 3), #  5  - branch if equal
        ("bne", op_bne, 3), #  6  - branch if not equal
        ("slt", op_slt, 4), #  7  - set if less than
        ("seq", op_seq, 4), #  8  - set if equal
        ("arb", op_arb, 2), #  9  - accumulate relative base
        ("hlt", op_hlt, 1)  # 10+ - halt
    )

    def print_instr(mem, ip):
        opcode = min(mem[ip] % 100, len(Intcode.opcodes) - 1)
        next_ip = ip + Intcode.opcodes[opcode][2]

        params = []
        for i in range(1, Intcode.opcodes[opcode][2]):
            mode = Intcode.getmode(mem[ip], i)
            if mode == 0:
                params.append("[" + str(mem[ip + i]) + "]")
            elif mode == 1:
                params.append(str(mem[ip + i]))
            elif mode == 2:
                params.append("(" + str(mem[ip + i]) + ")")
            else:
                params.append("?")

        sys.stdout.write(".    " + str(ip) + ":    ")
        sys.stdout.write(Intcode.opcodes[opcode][0] + "    ")
        sys.stdout.write(",    ".join(params))
        print()

    def print_asm(mem, prgm_size = None):
        if prgm_size is None:
            prgm_size = len(mem)

        ip = 0
        while ip < prgm_size:
            Intcode.print_instr(mem, ip)

            opcode = min(mem[ip] % 100, len(Intcode.opcodes) - 1)
            ip += Intcode.opcodes[opcode][2]

        print()


ram = Intcode.load_prgm("day11.input")
cpu = Intcode(ram)

pos = (0, 0)
dir = (0, 1)
tiles = {}
tiles_painted = 0
paint = True

def get_input():
    return 0 if pos not in tiles else tiles[pos]



k = 0
def handle_output(output):
    global pos
    global dir
    global tiles
    global tiles_painted
    global paint

    global k
    k += 1
    if k > 20:
        exit()
    print(pos, dir)
    
    if paint:
        # paint (output = color)
        print('output color %s' % output)
        if pos not in tiles:
            tiles_painted += 1

        tiles[pos] = output
    else:
        print('output turn %s' % output)
        if output == 0:
            # turn left
            x, y = dir
            dir = (-y, x)
        elif output == 1:
            # turn right
            x, y = dir
            dir = (y, -x)

        # move
        pos = tuple(map(sum, zip(pos, dir)))
        cpu.input(get_input())

    paint = not paint

    

cpu.add_output(handle_output)
cpu.input(get_input())
cpu.run()
print(tiles_painted)
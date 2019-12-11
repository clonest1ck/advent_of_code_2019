import math
from enum import Enum

class status(Enum):
    HALT = 1
    GET_INPUT = 2

class direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Memory(list):
    def keycheck(self, key):
        if self.__len__() <= key:
            diff = key - self.__len__()
            while diff >= 0:
                self.append(0)
                diff -= 1

    def __getitem__(self, key):
        self.keycheck(key)
        return list.__getitem__(self, key)

    def __setitem__(self, key, value):
        self.keycheck(key)
        return list.__setitem__(self, key, value)


def getInitialMemory():
    f = open("11dec-input", 'r')
    file_content = f.read()
    f.close()
    memory = Memory(map(int, file_content.split(',')))
    return memory

def getOpcode(inst):
    inst_str = str(inst)
    if len(inst_str) < 2:
        inst_str = "0" + inst_str
    opcode = int(inst_str[-2:])
    return opcode

def getArgs(inst, num, memory, pc, rc):
    inst_str = str(inst)
    if len(inst_str) < 2:
        inst_str = "0" + inst_str

    modes = list(inst_str[:-2])
    modes.reverse()

    args = []
    for i in range(num):
        if len(modes) <= i:
            modes += "0"
        mode = int(modes[i])

        arg = 0
        if (mode == 0):
            addr = memory[pc]
        elif (mode == 1):
            addr = pc
        elif (mode == 2):
            addr = memory[pc] + rc
        else:
            print("Unknown mode: %d at %d" % (mode, pc))
            exit()
        args.append(addr)
        pc += 1
    return args

def run(memory, inputs, pc = 0, rc = 0):
    outputs = []

    while(True):
        instr = memory[pc]
        opcode = getOpcode(instr)
        pc += 1
        result = 0
        addr = -1

        if (opcode == 99):
            break
        elif (opcode == 1):
            args = getArgs(instr, 3, memory, pc, rc)
            arg1 = memory[args[0]]
            arg2 = memory[args[1]]
            addr = args[2]
            pc += 3
            result = arg1 + arg2
        elif (opcode == 2):
            args = getArgs(instr, 3, memory, pc, rc)
            arg1 = memory[args[0]]
            arg2 = memory[args[1]]
            addr = args[2]
            pc += 3
            result = arg1 * arg2
        elif (opcode == 3):
            if len(inputs) == 0:
                return [status.GET_INPUT, pc - 1, rc, outputs]
            result = int(inputs.pop(0))
            args = getArgs(instr, 1, memory, pc, rc)
            addr = args[0]
            pc += 1
        elif (opcode == 4):
            args = getArgs(instr, 1, memory, pc, rc)
            arg1 = memory[args[0]]
            pc += 1
            outputs.append(arg1)
        elif (opcode == 5):
            args = getArgs(instr, 2, memory, pc, rc)
            arg1 = memory[args[0]]
            pc += 2
            if (arg1 != 0):
                pc = memory[args[1]]
        elif (opcode == 6):
            args = getArgs(instr, 2, memory, pc, rc)
            arg1 = memory[args[0]]
            pc += 2
            if (arg1 == 0):
                pc = memory[args[1]]
        elif (opcode == 7):
            args = getArgs(instr, 3, memory, pc, rc)
            arg1 = memory[args[0]]
            arg2 = memory[args[1]]
            addr = args[2]
            pc += 3
            if (arg1 < arg2):
                result = 1
            else:
                result = 0
        elif (opcode == 8):
            args = getArgs(instr, 3, memory, pc, rc)
            arg1 = memory[args[0]]
            arg2 = memory[args[1]]
            addr = args[2]
            pc += 3
            if (arg1 == arg2):
                result = 1
            else:
                result = 0
        elif (opcode == 9):
            args = getArgs(instr, 1, memory, pc, rc)
            arg1 = memory[args[0]]
            pc += 1
            rc += arg1
        else:
            print ("Unknown opcode")
            exit()

        if addr != -1:
            memory[addr] = result

    return [status.HALT, 0, 0, outputs]

def move(start, direction, turn):
    if turn == 0:
        turn = direction.LEFT
    elif turn == 1:
        turn = direction.RIGHT

    delta = (0, 0)
    if direction == direction.UP or direction == direction.DOWN:
        if turn == direction.LEFT:
            delta = (-1, 0)
        elif turn == direction.RIGHT:
            delta = (1, 0)
    elif direction == direction.RIGHT or direction == direction.LEFT:
        if turn == direction.LEFT:
            delta = (0, 1)
        elif turn == direction.RIGHT:
            delta = (0, -1)

    if direction == direction.DOWN or direction == direction.LEFT:
        (x, y) = delta
        delta = (x * -1, y * -1)

    (sx, sy) = start
    (dx, dy) = delta
    if dx < 0:
        direction = direction.LEFT
    elif dx > 0:
        direction = direction.RIGHT
    elif dy < 0:
        direction = direction.DOWN
    elif dy > 0:
        direction = direction.UP

    return ((sx + dx, sy + dy), direction)


def paint(start = 0):
    memory = getInitialMemory()
    facing = direction.UP
    visited = dict()
    pos = (0, 0)
    visited[pos] = start
    code = status.GET_INPUT
    pc = 0
    rc = 0

    while code != status.HALT:
        if not pos in visited:
            visited[pos] = 0
        color = visited[pos]
        out = run(memory, [color], pc, rc)
        code = out[0]
        pc = out[1]
        rc = out[2]
        output = out[3]
        color = output[0]
        turn = output[1]
        visited[pos] = color

        (pos, facing) = move(pos, facing, turn)

    return visited

painted = paint()

print("Part 1: %s" % len(painted.keys()))

painted = paint(1)
min_x = math.inf
min_y = math.inf
max_x = -math.inf
max_y = -math.inf

for tile in painted:
    (x, y) = tile
    if min_x > x:
        min_x = x
    if max_x < x:
        max_x = x
    if min_y > y:
        min_y = y
    if max_y < y:
        max_y = y

x_range = range(min_x, max_x + 1)
y_range = list(reversed(range(min_y, max_y + 1)))

canvas = [[" " for m in x_range] for b in y_range]

for tile in painted:
    if painted[tile] == 0:
        continue
    (xc, yc) = tile
    x = x_range.index(xc)
    y = y_range.index(yc)
    canvas[y][x] = "#"

for line in canvas:
    print("".join(line))




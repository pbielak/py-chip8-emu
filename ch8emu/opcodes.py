"""
Implementation of opcodes
"""
import random


class OpcodeNotSupportedError(Exception):
    pass


class UnknownOpcodeError(Exception):
    pass


def execute_opcode(opcode, emulator):
    opcode_fns = {
        0x0000: x0___,
        0x1000: x1nnn,
        0x2000: x2nnn,
        0x3000: x3xkk,
        0x4000: x4xkk,
        0x5000: x5xy0,
        0x6000: x6xkk,
        0x7000: x7xkk,
        0x8000: x8xy_,
        0x9000: x9xy0,
        0xA000: xAnnn,
        0xB000: xBnnn,
        0xC000: xCxkk,
        0xD000: xDxyn,
        0xE000: xEx__,
        0xF000: xFx__,
    }

    opcode_prefix = opcode & 0xF000
    fn = opcode_fns[opcode_prefix]
    fn(opcode, emulator)


def x0___(opcode, emulator):
    if opcode == 0x00E0:
        emulator.logger.log('CLS')

        for idx in range(len(emulator.gfx)):
            emulator.gfx[idx] = 0

        emulator.draw_flag = True
        emulator.pc += 2

    elif opcode == 0x00EE:
        emulator.logger.log('RET')

        emulator.pc = emulator.stack[emulator.sp]
        emulator.sp -= 1

    else:
        nnn = opcode & 0x0FFF
        if nnn == 0x000:
            nnn = 0x200

        emulator.logger.log('SYS %s' % format(nnn, '#05x'))
        emulator.pc = nnn


def x1nnn(opcode, emulator):
    emulator.logger.log('JP addr')
    emulator.pc = opcode & 0x0FFF


def x2nnn(opcode, emulator):
    emulator.logger.log('CALL addr')
    emulator.stack[emulator.sp] = emulator.pc
    emulator.sp += 1
    emulator.pc = opcode & 0x0FFF


def x3xkk(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    kk = opcode & 0x00FF
    emulator.logger.log('SE V%s, %s' % (format(x, 'X'), format(kk, '#04x')))

    if emulator.V[x] == kk:
        emulator.pc += 4
    else:
        emulator.pc += 2


def x4xkk(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    kk = opcode & 0x00FF
    emulator.logger.log('SNE V%s, %s' % (format(x, 'X'), format(kk, '#04x')))

    if emulator.V[x] != kk:
        emulator.pc += 4
    else:
        emulator.pc += 2


def x5xy0(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    emulator.logger.log('SE V%s, V%s' % (format(x, 'X'), format(y, 'X')))

    if emulator.V[x] == emulator.V[y]:
        emulator.pc += 4
    else:
        emulator.pc += 2


def x6xkk(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    kk = opcode & 0x00FF
    emulator.logger.log('LD V%s, %s' % (format(x, 'X'), format(kk, '#04x')))

    emulator.V[x] = kk
    emulator.pc += 2


def x7xkk(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    kk = opcode & 0x00FF
    emulator.logger.log('ADD V%s, %s' % (format(x, 'X'), format(kk, '#04x')))

    emulator.V[x] += kk
    emulator.pc += 2


def x8xy_(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    op = opcode & 0x000F

    if op == 0x0:
        emulator.logger.log('LD V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[x] = emulator.V[y]
    elif op == 0x1:
        emulator.logger.log('OR V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[x] = emulator.V[x] | emulator.V[y]
    elif op == 0x2:
        emulator.logger.log('AND V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[x] = emulator.V[x] & emulator.V[y]
    elif op == 0x3:
        emulator.logger.log('XOR V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[x] = emulator.V[x] ^ emulator.V[y]
    elif op == 0x4:
        emulator.logger.log('ADD V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[x] = emulator.V[x] + emulator.V[y]
        emulator.V[0xF] = 1 if emulator.V[x] > 0xFF else 0
    elif op == 0x5:
        emulator.logger.log('SUB V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[0xF] = 1 if emulator.V[x] > emulator.V[y] else 0
        emulator.V[x] = emulator.V[x] - emulator.V[y]
    elif op == 0x6:
        emulator.logger.log('SHR V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[0xF] = emulator.V[x] & 0x01
        emulator.V[x] = emulator.V[x] >> 1
    elif op == 0x7:
        emulator.logger.log('SUBN V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[0xF] = 1 if emulator.V[y] > emulator.V[x] else 0
        emulator.V[x] = emulator.V[y] - emulator.V[x]
    elif op == 0xE:
        emulator.logger.log('SHL V%s, V%s' % (format(x, 'X'), format(y, 'X')))
        emulator.V[0xF] = emulator.V[x] & 0x80
        emulator.V[x] = emulator.V[x] << 1
    else:
        raise UnknownOpcodeError('Unknown opcode: {}'.format(opcode, '#06x'))

    emulator.pc += 2


def x9xy0(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    emulator.logger.log('SNE V%s, V%s' % (format(x, 'X'), format(y, 'X')))

    if emulator.V[x] != emulator.V[y]:
        emulator.pc += 4
    else:
        emulator.pc += 2


def xAnnn(opcode, emulator):
    nnn = opcode & 0x0FFF
    emulator.logger.log('LD I, %s' % (format(nnn, '#05x')))

    emulator.I = nnn
    emulator.pc += 2


def xBnnn(opcode, emulator):
    nnn = opcode & 0x0FFF
    emulator.logger.log('JP V0, %s' % (format(nnn, '#05x')))
    emulator.pc = nnn + emulator.V[0x0]


def xCxkk(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    kk = opcode & 0x00FF
    emulator.logger.log('RND V%s, %s' % (format(x, 'X'), format(kk, '#04x')))

    rnd = random.randint(0, 255)

    emulator.V[x] = rnd & kk
    emulator.pc += 2


def xDxyn(opcode, emulator):
    x = emulator.V[(opcode & 0x0F00) >> 8]
    y = emulator.V[(opcode & 0x00F0) >> 4]
    n = opcode & 0x000F

    emulator.logger.log('DRW V%s, V%s, %s' % (format(x, 'X'),
                                              format(y, 'X'),
                                              format(n, 'X')))

    emulator.V[0xF] = 0
    for yline in range(n):
        pixel = emulator.memory[emulator.I + yline]
        for xline in range(8):
            if (pixel & (0x80 >> xline)) != 0:
                if emulator.gfx[((y + yline) * 64) + x + xline] == 1:
                    emulator.V[0xF] = 1

                emulator.gfx[((y + yline) * 64) + x + xline] ^= 1

    emulator.draw_flag = True
    emulator.pc += 2


def xEx__(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    op = opcode & 0x00FF

    if op == 0x9E:
        emulator.logger.log('SKP V%s' % (format(x, 'X')))
        if emulator.key[emulator.V[x]] == 1:
            emulator.pc += 2

    elif op == 0xA1:
        emulator.logger.log('SKNP V%s' % (format(x, 'X')))
        if emulator.key[emulator.V[x]] == 0:
            emulator.pc += 2

    else:
        raise UnknownOpcodeError('Unknown opcode: {}'.format(opcode, '#06x'))

    emulator.pc += 2


def xFx__(opcode, emulator):
    x = (opcode & 0x0F00) >> 8
    op = opcode & 0x00FF

    if op == 0x07:
        emulator.logger.log('LD V%s, DT' % (format(x, 'X')))
        emulator.V[x] = emulator.delay_timer
        emulator.pc += 2

    elif op == 0x0A:
        emulator.logger.log('LD V%s, K' % (format(x, 'X')))
        for i in range(16):
            if emulator.key[i] == 1:
                emulator.V[x] = i
                emulator.pc += 2
                break

    elif op == 0x15:
        emulator.logger.log('LD DT, V%s' % (format(x, 'X')))
        emulator.delay_timer = emulator.V[x]
        emulator.pc += 2

    elif op == 0x18:
        emulator.logger.log('LD ST, V%s' % (format(x, 'X')))
        emulator.sound_timer = emulator.V[x]
        emulator.pc += 2

    elif op == 0x1E:
        emulator.logger.log('ADD I, V%s' % (format(x, 'X')))
        emulator.I = emulator.I + emulator.V[x]
        emulator.pc += 2

    elif op == 0x29:
        emulator.logger.log('LD F, V%s' % (format(x, 'X')))
        emulator.I = 0x050 + 5 * emulator.V[x]
        emulator.pc += 2

    elif op == 0x33:
        emulator.logger.log('LD B, V%s' % (format(x, 'X')))
        Vx = emulator.V[x]
        Vx_100 = (Vx // 100) % 100
        Vx_10 = (Vx // 10) % 10
        Vx_1 = (Vx - 100 * Vx_100 - 10 * Vx_10)

        emulator.memory[emulator.I] = Vx_100
        emulator.memory[emulator.I + 1] = Vx_10
        emulator.memory[emulator.I + 2] = Vx_1
        emulator.pc += 2

    elif op == 0x55:
        emulator.logger.log('LD [I], V%s' % (format(x, 'X')))
        for idx in range(16):
            emulator.memory[emulator.I + idx] = emulator.V[idx]

        emulator.pc += 2

    elif op == 0x65:
        emulator.logger.log('LD V%s, [I]' % (format(x, 'X')))
        for idx in range(16):
            emulator.V[idx] = emulator.memory[emulator.I + idx]

        emulator.pc += 2

    else:
        raise UnknownOpcodeError('Unknown opcode: {}'.format(opcode, '#06x'))

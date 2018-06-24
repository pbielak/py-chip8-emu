"""
Util functions
"""


def print_memory(emulator, cells_per_row=16):
    for idx in range(len(emulator.memory)):
        if idx % cells_per_row == 0:
            idx_str = '[%4d | %5s] ' % (
                idx,
                format(idx, '#04X').replace('X', 'x')
            )
            print(f'\n{idx_str}', end='')

        print(format(emulator.memory[idx], '#04X').replace('X', 'x'), end=' ')


class InstructionLogger(object):
    """Assembly instruction logger"""
    def __init__(self):
        self.enabled = None

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def log(self, msg):
        if self.enabled:
            print('Executing:', msg)


def draw_gfx(gfx):
    pass
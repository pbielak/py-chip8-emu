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
    def __init__(self, display=None):
        self.display = display
        self.enabled = None

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def log(self, msg):
        if self.enabled:
            if not self.display:
                print('Executing:', msg)
            else:
                self.display.add_instruction(msg)


def draw_gfx(display, gfx, width, height):
    for y in range(height):
        for x in range(width):
            ch = '*' if gfx[y * width + x] == 1 else ' '
            display.draw_on_canvas(2 * x, y, ch)
            display.draw_on_canvas(2 * x + 1, y, ' ')

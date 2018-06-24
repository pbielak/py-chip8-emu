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

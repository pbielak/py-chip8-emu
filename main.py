"""Chip-8 emulator"""
from ch8emu import emulator
from ch8emu import utils


def main():

    emu = emulator.Emulator()
    emu.load_rom('roms/chip8_emulator_logo.ch8')

    #utils.print_memory(emu)
    for _ in range(1):
        emu.run_single_cycle()


if __name__ == '__main__':
    main()

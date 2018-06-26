"""Chip-8 emulator"""
import argparse
from time import sleep

from ch8emu import emulator
from ch8emu import ncurses_display as ncd
from ch8emu import opcodes
from ch8emu import utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rom-file', help='Path to ROM', type=str)
    return parser.parse_args()


def main():
    args = parse_args()

    display = ncd.NCursesDisplay()

    il = utils.InstructionLogger(display)
    il.enable()

    emu = emulator.Emulator(logger=il)
    emu.load_rom(args.rom_file)

    try:
        while True:
            emu.run_single_cycle()

            if emu.draw_flag:
                emu.draw_flag = False
                utils.draw_gfx(display, emu.gfx, 64, 32)

            sleep(0.05)

    except KeyboardInterrupt:
        print('Ctrl-C pressed!')
    except (opcodes.UnknownOpcodeError,
            opcodes.OpcodeNotSupportedError) as e:
        print(str(e))

    display.cleanup()


if __name__ == '__main__':
    main()


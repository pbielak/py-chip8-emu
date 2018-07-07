"""Chip-8 emulator"""
import argparse
import curses
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

    curses.curs_set(0)

    display.stdscr.nodelay(True)  # Non-blocking getch()
    curses.noecho()
    keyboard = ['1', '2', '3', 'C',
                '4', '5', '6', 'D',
                '7', '8', '9', 'E',
                'A', '0', 'B', 'F']
    keyboard = [ord(k) for k in keyboard]

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

            emu.key = [0] * 16
            c = display.stdscr.getch()
            if c != -1 and c in keyboard:
                emu.key[keyboard.index(c)] = 1

            curses.flushinp()
            sleep(0.05)

    except KeyboardInterrupt:
        print('Ctrl-C pressed!')
    except (opcodes.UnknownOpcodeError,
            opcodes.OpcodeNotSupportedError) as e:
        print(str(e))

    display.cleanup()


if __name__ == '__main__':
    main()


"""Chip-8 emulator"""
from time import sleep

from ch8emu import emulator
from ch8emu import ncurses_display as ncd
from ch8emu import opcodes
from ch8emu import utils


def main():
    display = ncd.NCursesDisplay()

    il = utils.InstructionLogger(display)
    il.enable()

    emu = emulator.Emulator(logger=il)
    emu.load_rom('roms/chip8_picture.ch8')

    #utils.print_memory(emu)
    try:
        while True:
            emu.run_single_cycle()

            if emu.draw_flag:
                emu.draw_flag = False
                utils.draw_gfx(display, emu.gfx, 64, 32)

            sleep(0.1)

    except KeyboardInterrupt:
        print('Ctrl-C pressed!')
    except (opcodes.UnknownOpcodeError,
            opcodes.OpcodeNotSupportedError) as e:
        print(str(e))

    display.cleanup()


if __name__ == '__main__':
    main()

"""Chip-8 emulator"""
from time import sleep

from ch8emu import emulator
from ch8emu import opcodes
from ch8emu import utils


def main():

    il = utils.InstructionLogger()
    il.enable()

    emu = emulator.Emulator(logger=il)
    emu.load_rom('roms/chip8_emulator_logo.ch8')

    #utils.print_memory(emu)
    while True:
        try:
            emu.run_single_cycle()

            if emu.draw_flag:
                emu.draw_flag = False
                utils.draw_gfx(emu.gfx, 64, 32)

        except KeyboardInterrupt:
            print('Ctrl-C pressed!')
            break
        except (opcodes.UnknownOpcodeError,
                opcodes.OpcodeNotSupportedError) as e:
            print(str(e))
            break

        sleep(1)


if __name__ == '__main__':
    main()

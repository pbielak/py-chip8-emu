"""Chip-8 emulator"""
from time import sleep

from ch8emu import emulator
from ch8emu import opcodes
from ch8emu import utils


def main():

    emu = emulator.Emulator()
    emu.load_rom('roms/chip8_emulator_logo.ch8')

    #utils.print_memory(emu)
    while True:
        try:
            emu.run_single_cycle()
        except KeyboardInterrupt:
            print('Ctrl-C pressed!')
            break
        except (opcodes.UnknownOpcodeError,
                opcodes.OpcodeNotSupportedError) as e:
            print(e.message)
            break

        sleep(0.5)


if __name__ == '__main__':
    main()

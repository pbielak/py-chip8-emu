"""
Actual emulator class
"""
from ch8emu import opcodes
from ch8emu import sprites


class Emulator(object):
    MEMORY_SIZE = 4096
    NB_V_REGISTERS = 16
    STACK_SIZE = 16
    GFX_SIZE = 64 * 32
    KEYPAD_SIZE = 16

    def __init__(self, logger):
        self.logger = logger

        self.pc = None
        self.stack = None

        self.sp = None
        self.memory = None

        self.V = None
        self.I = None

        self.delay_timer = None
        self.sound_timer = None

        self.gfx = None
        self.key = None

        self.draw_flag = None

        self.reset()

    def reset(self):
        self.pc = 0x200

        self.stack = [0x0] * self.STACK_SIZE
        self.sp = 0

        self.memory = [0x00] * self.MEMORY_SIZE
        self._load_sprites()

        self.V = [0x0] * self.NB_V_REGISTERS
        self.I = 0x0

        self.gfx = [0] * self.GFX_SIZE
        self.key = [0] * self.KEYPAD_SIZE

        self.delay_timer = 0
        self.sound_timer = 0

        self.draw_flag = False

    def _load_sprites(self):
        sprites_data = sprites.get_sprites()

        for idx in range(len(sprites_data)):
            self.memory[idx] = sprites_data[idx]

    def load_rom(self, filename):
        with open(filename, 'rb') as f:
            rom_buffer = f.read()

        for idx in range(len(rom_buffer)):
            self.memory[0x200 + idx] = rom_buffer[idx]

    def run_single_cycle(self):
        opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
        opcodes.execute_opcode(opcode, self)

        self._update_timers()

    def _update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            if self.sound_timer == 1:
                print('BEEP!')

            self.sound_timer -= 1

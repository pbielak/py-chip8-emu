"""
N-Curses based interface (GUI)
"""
import curses


class NCursesDisplay(object):
    CANVAS_WIDTH = 128
    CANVAS_HEIGHT = 32
    INSTR_WIDTH = 32
    INSTR_HEIGHT = 32

    def __init__(self):
        self.stdscr = curses.initscr()
        self._ensure_terminal_size_correct()

        self.stdscr.clear()
        self.canvas_win = curses.newwin(self.CANVAS_HEIGHT + 2,
                                        self.CANVAS_WIDTH + 2,
                                        0, 0)
        self.canvas_win.border()
        self.canvas_win.refresh()

        self.instruction_win = curses.newwin(self.INSTR_HEIGHT + 2,
                                             self.INSTR_WIDTH + 2,
                                             0, self.CANVAS_WIDTH + 3)
        self.instruction_rows = 0

        self.instruction_win.scrollok(True)
        self.instruction_win.addstr('\n')
        self.instruction_win.border()
        self.instruction_win.refresh()

    def _ensure_terminal_size_correct(self):
        y_max, x_max = self.stdscr.getmaxyx()
        if y_max != self.CANVAS_HEIGHT + 2 and \
           x_max != (self.CANVAS_WIDTH + 2) + (self.INSTR_WIDTH + 2) + 1:
            curses.endwin()
            print('Screen must be {} x {}'.format(
                (self.CANVAS_WIDTH + 2) + (self.INSTR_WIDTH + 2),
                self.CANVAS_HEIGHT + 2))
            quit()

    def draw_on_canvas(self, x, y, ch):
        self.canvas_win.addstr(y + 1, x + 1, ch)
        self.canvas_win.refresh()

    def add_instruction(self, msg):
        self.instruction_win.addstr(f' [{self.instruction_rows}] {msg}\n')
        self.instruction_win.border()
        self.instruction_win.refresh()
        self.instruction_rows += 1

    def cleanup(self):
        curses.endwin()

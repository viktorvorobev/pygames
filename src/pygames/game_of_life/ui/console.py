import blessed

from pygames.game_of_life import game_of_life as gof

BOUNDARIES_WIDTH = 1
EXIT_KEYS = ('q', 'Q')
BOUNDARIES_KEYS = ('b', 'B')
RESTART_KEYS = ('r', 'R')


class TerminalController:   # pylint: disable = too-few-public-methods
    DEFAULT_TIMEOUT = 0.02  # seconds

    def __init__(self, terminal: blessed.Terminal, game: gof.GameOfLife):
        self.term = terminal
        self.width = terminal.width
        self.height = terminal.height - BOUNDARIES_WIDTH * 2
        self.game = game

        with self.term.cbreak(), self.term.hidden_cursor():
            print(self.term.home + self.term.clear, end='')
        self._old_population = 0

    def run(self):  # pragma: nocover
        with self.term.cbreak(), self.term.hidden_cursor():
            while (key := self.term.inkey(timeout=self.DEFAULT_TIMEOUT)) not in EXIT_KEYS:
                self._process_key(key)
                self._render_screen()
                self.game.update()

    def _render_screen(self):
        self._show_population(self.game.population)
        self._show_cells()
        self._show_instructions()

    def _process_key(self, key):
        if key in BOUNDARIES_KEYS:
            self.game.boundaries = not self.game.boundaries
        if key in RESTART_KEYS:
            self.game.reset_state()

    def _show_population(self, population):
        old_population_len = len(str(self._old_population))
        new_population_len = len(str(population))
        if new_population_len < old_population_len:
            population = str(population).rjust(old_population_len)
        self._old_population = population
        txt_erase = self.term.move_xy(0, 0)
        print(txt_erase + f'Population: {population}', end='', flush=True)

    def _show_cells(self):
        for row_num, row in enumerate(self.game.state):
            for col_num, cell in enumerate(row):
                txt_erase = self.term.move_xy(col_num, row_num + BOUNDARIES_WIDTH)
                symbol = '*' if cell == gof.LIVE else ' '
                print(txt_erase + symbol, end='', flush=True)

    def _show_instructions(self):
        txt_erase = self.term.move_xy(0, self.term.height - 1)
        exit_text = 'Exit: "Q"'
        boundaries = f'Toggle boundaries: "B" ({"on" if self.game.boundaries else "off"})'
        restart = 'Restart: "R"'
        print(txt_erase + ', '.join((exit_text, restart, boundaries)), end='')


def main():  # pragma: nocover
    term = blessed.Terminal()
    width, height = term.width, term.height - BOUNDARIES_WIDTH * 2
    game = gof.GameOfLife(width=width, height=height, boundaries=True)
    controller = TerminalController(terminal=term, game=game)
    controller.run()


if __name__ == '__main__':  # pragma: nocover
    main()

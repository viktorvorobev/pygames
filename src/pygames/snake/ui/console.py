from functools import partial

import blessed

from pygames import snake

display = partial(print, end='', flush=True)

BOUNDARIES_WIDTH = 1
EXIT_KEYS = ('q', 'Q')
BOUNDARIES_KEYS = ('b', 'B')
RESTART_KEYS = ('r', 'R')


class DirectionKeys:  # pylint: disable = too-few-public-methods
    UP = ('w', 'W')
    DOWN = ('s', 'S')
    LEFT = ('a', 'A')
    RIGHT = ('d', 'D')


class TerminalController:  # pylint: disable = too-few-public-methods
    DEFAULT_TIMEOUT = 0.1  # seconds
    FRUIT_SYMBOL = 'X'
    HEAD_SYMBOL = 'O'
    BODY_SYMBOL = 'o'

    def __init__(self, terminal: blessed.Terminal, game: snake.Snake):
        self.term = terminal
        self.width = terminal.width
        self.height = terminal.height - BOUNDARIES_WIDTH * 2
        self.game = game
        self.game_over = False

        with self.term.cbreak(), self.term.hidden_cursor():
            display(self.term.home + self.term.clear, end='')

    def run(self):  # pragma: nocover
        with self.term.cbreak(), self.term.hidden_cursor():
            while (key := self.term.inkey(timeout=self.DEFAULT_TIMEOUT)) not in EXIT_KEYS:
                self._process_key(key)
                if self.game_over:
                    continue
                self._render_screen()
                try:
                    self.game.update()
                except snake.GameOverException:
                    self.game_over = True
                if self.game_over:
                    self._show_game_over()

    def _render_screen(self):
        self._show_score()
        self._show_snake()
        self._show_fruit()
        self._show_instructions()

    def _process_key(self, key):
        if key in BOUNDARIES_KEYS:
            self.game.boundaries = not self.game.boundaries
        if key in RESTART_KEYS:
            self.game_over = False
            self.game.reset_state()
        if key in DirectionKeys.UP:
            self.game.direction = snake.Direction.UP
        if key in DirectionKeys.DOWN:
            self.game.direction = snake.Direction.DOWN
        if key in DirectionKeys.LEFT:
            self.game.direction = snake.Direction.LEFT
        if key in DirectionKeys.RIGHT:
            self.game.direction = snake.Direction.RIGHT

    def _show_score(self):
        txt_erase = self.term.move_xy(0, 0)
        display(txt_erase + f'Score: {self.game.score}')

    def _show_snake(self):
        self.__clear_snake_field()
        head_x, head_y = self.game.snake[0]
        txt_erase = self.term.move_xy(head_x, head_y + BOUNDARIES_WIDTH)
        display(txt_erase + self.HEAD_SYMBOL)
        for body_x, body_y in self.game.snake[1:]:
            txt_erase = self.term.move_xy(body_x, body_y + BOUNDARIES_WIDTH)
            display(txt_erase + self.BODY_SYMBOL)

    def __clear_snake_field(self):
        txt_erase = self.term.move_xy(0, 1)
        display(txt_erase + ' ' * self.width * self.height)

    def _show_fruit(self):
        fruit_x, fruit_y = self.game.fruit
        txt_erase = self.term.move_xy(fruit_x, fruit_y + BOUNDARIES_WIDTH)
        display(txt_erase + self.FRUIT_SYMBOL)

    def _show_instructions(self):
        txt_erase = self.term.move_xy(0, self.term.height - 1)
        controls_text = 'Controls: "WASD"'
        exit_text = 'Exit: "Q"'
        restart = 'Restart: "R"'
        boundaries = f'Toggle boundaries: "B" ({"on" if self.game.boundaries else "off"})'
        display(txt_erase + ', '.join((controls_text, exit_text, restart, boundaries)))

    def _show_game_over(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            display(self.term.home + self.term.clear)
        self._show_score()
        self._show_instructions()

        game_over_text = 'GAME OVER'
        txt_erase = self.term.move_xy(self.width // 2 - len(game_over_text) // 2, self.height // 2)
        display(txt_erase + game_over_text)


def main():  # pragma: nocover
    term = blessed.Terminal()
    width, height = term.width, term.height - BOUNDARIES_WIDTH * 2
    game = snake.Snake(width=width, height=height, boundaries=True)
    controller = TerminalController(terminal=term, game=game)
    controller.run()


if __name__ == '__main__':  # pragma: nocover
    main()

import copy

import blessed
import pytest

from pygames.snake.snake import Snake, Direction
from pygames.snake.ui import console


# pylint: disable = protected-access


@pytest.fixture(name='controller')
def controller_fixture():
    term = blessed.Terminal()
    width, height = term.width, term.height - console.BOUNDARIES_WIDTH * 2
    game = Snake(width=width, height=height, boundaries=False)
    yield console.TerminalController(terminal=term, game=game)


def test_created(controller, capsys):
    assert controller
    assert controller.width == 80
    assert controller.height == 23
    captured = capsys.readouterr()
    assert captured.out == ''


def test_rendered(controller: console.TerminalController, capsys):
    controller._render_screen()
    captured = capsys.readouterr()
    output = captured.out

    score_string = f'Score: {controller.game.score}'
    assert output.startswith(score_string), repr(output)
    output = output.replace(score_string, '')

    instructions_string = 'Controls: "WASD", Exit: "Q", Restart: "R", Toggle boundaries: "B" (off)'
    assert output.endswith(instructions_string), repr(output)
    output = output.replace(instructions_string, '')
    # 1 symbol for fruit, 1 for head and rest for body
    assert len(output) == (controller.game.width * controller.game.height) + 2 + controller.game.score
    assert output.count(controller.FRUIT_SYMBOL) == 1
    assert output.count(controller.HEAD_SYMBOL) == 1
    assert output.count(controller.BODY_SYMBOL) == controller.game.score


def test_rendered_snake_with_body(controller: console.TerminalController, capsys):
    snake_head = controller.game.snake[0]
    controller.game.fruit = [snake_head[0] + 1, snake_head[1]]
    controller.game.update()
    controller._render_screen()
    captured = capsys.readouterr()

    output = captured.out

    score_string = f'Score: {controller.game.score}'
    assert output.startswith(score_string), repr(output)
    output = output.replace(score_string, '')
    instructions_string = 'Controls: "WASD", Exit: "Q", Restart: "R", Toggle boundaries: "B" (off)'
    assert output.endswith(instructions_string), repr(output)
    output = output.replace(instructions_string, '')
    # 1 symbol for fruit, 1 for head and rest for body
    assert len(output) == (controller.game.width * controller.game.height) + 2 + controller.game.score
    assert output.count(controller.FRUIT_SYMBOL) == 1
    assert output.count(controller.HEAD_SYMBOL) == 1
    assert output.count(controller.BODY_SYMBOL) == controller.game.score


def test_show_score(controller: console.TerminalController, capsys):
    controller._show_score()
    captured = capsys.readouterr()
    assert captured.out == f'Score: {controller.game.score}', repr(captured.out)


def test_show_score_overrides(controller: console.TerminalController, capsys):
    for score in (1, 10, 100):
        controller.game.score = score
        controller._show_score()
        captured = capsys.readouterr()
        assert captured.out == f'Score: {controller.game.score}', repr(captured.out)


def test_show_menu(controller: console.TerminalController, capsys):
    controller._show_instructions()
    captured = capsys.readouterr()
    assert captured.out == 'Controls: "WASD", Exit: "Q", Restart: "R", Toggle boundaries: "B" (off)', repr(captured.out)


def test_show_game_over(controller: console.TerminalController, capsys):
    controller._show_game_over()
    captured = capsys.readouterr()
    output = captured.out

    score_string = f'Score: {controller.game.score}'
    assert output.startswith(score_string), repr(output)
    output = output.replace(score_string, '')

    instructions_string = 'Controls: "WASD", Exit: "Q", Restart: "R", Toggle boundaries: "B" (off)'
    assert output.startswith(instructions_string), repr(output)
    output = output.replace(instructions_string, '')
    assert 'GAME OVER' == output


def test_process_reset_key(controller: console.TerminalController):
    for key in console.RESTART_KEYS:
        controller.game.update()
        controller.game.update()
        controller.game.update()
        initial_snake = copy.deepcopy(controller.game.snake)
        controller._process_key(key)
        assert controller.game.snake != initial_snake


def test_process_boundaries_key(controller: console.TerminalController):
    for key in console.BOUNDARIES_KEYS:
        old_state = controller.game.boundaries
        controller._process_key(key)
        assert old_state != controller.game.boundaries


def test_menu_changes_boundaries(controller: console.TerminalController, capsys):
    controller._show_instructions()
    captured = capsys.readouterr()
    boundaries_state = 'on' if controller.game.boundaries else 'off'
    assert captured.out == f'Controls: "WASD", Exit: "Q", Restart: "R", Toggle boundaries: "B" ({boundaries_state})'

    controller.game.boundaries = not controller.game.boundaries
    controller._show_instructions()
    captured = capsys.readouterr()
    boundaries_state = 'on' if controller.game.boundaries else 'off'
    assert captured.out == f'Controls: "WASD", Exit: "Q", Restart: "R", Toggle boundaries: "B" ({boundaries_state})'


@pytest.mark.parametrize(
    'direction_keys,initial_direction,expected_direction',
    [
        (console.DirectionKeys.UP, Direction.LEFT, Direction.UP),
        (console.DirectionKeys.DOWN, Direction.LEFT, Direction.DOWN),
        (console.DirectionKeys.LEFT, Direction.UP, Direction.LEFT),
        (console.DirectionKeys.RIGHT, Direction.UP, Direction.RIGHT),
    ]
)
def test_process_direction_keys(
        controller: console.TerminalController, direction_keys,
        initial_direction: Direction, expected_direction: Direction):
    for key in direction_keys:
        controller.game._direction = initial_direction
        controller._process_key(key)
        assert controller.game.direction == expected_direction

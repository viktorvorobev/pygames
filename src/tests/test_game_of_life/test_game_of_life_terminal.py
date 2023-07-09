import copy

import blessed
import pytest

from pygames.game_of_life.game_of_life import GameOfLife
from pygames.game_of_life.ui import console


# pylint: disable = protected-access

@pytest.fixture(name='controller')
def controller_fixture():
    term = blessed.Terminal()
    width, height = term.width, term.height - console.BOUNDARIES_WIDTH * 2
    game = GameOfLife(width=width, height=height, boundaries=False)
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

    population_string = f'Population: {controller.game.population}'
    assert output.startswith(population_string), repr(output)
    output = output.replace(population_string, '')

    instructions_string = 'Exit: "Q", Restart: "R", Toggle boundaries: "B" (off)'
    assert output.endswith(instructions_string), repr(output)
    output = output.replace(instructions_string, '')

    assert len(output) == controller.game._width * controller.game._height
    assert output.count(controller.LIVE_SYMBOL) == controller.game.population


def test_show_population(controller: console.TerminalController, capsys):
    controller._show_population(controller.game.population)
    captured = capsys.readouterr()
    assert captured.out == f'Population: {controller.game.population}', repr(captured.out)


def test_show_population_shortens(controller: console.TerminalController, capsys):
    controller._show_population(10)
    captured = capsys.readouterr()
    assert captured.out == f'Population: {10}', repr(captured.out)
    controller._show_population(1)
    captured = capsys.readouterr()
    assert captured.out == f'Population:  {1}', repr(captured.out)


def test_show_menu(controller: console.TerminalController, capsys):
    controller._show_instructions()
    captured = capsys.readouterr()
    assert captured.out == 'Exit: "Q", Restart: "R", Toggle boundaries: "B" (off)', repr(captured.out)


def test_process_reset_key(controller: console.TerminalController):
    for key in console.RESTART_KEYS:
        old_state = copy.deepcopy(controller.game.state)
        controller._process_key(key)
        assert old_state != controller.game.state


def test_process_boundaries_key(controller: console.TerminalController):
    for key in console.BOUNDARIES_KEYS:
        old_state = controller.game.boundaries
        controller._process_key(key)
        assert old_state != controller.game.boundaries


def test_menu_changes_boundaries(controller: console.TerminalController, capsys):
    controller._show_instructions()
    captured = capsys.readouterr()
    boundaries_state = 'on' if controller.game.boundaries else 'off'
    assert captured.out == f'Exit: "Q", Restart: "R", Toggle boundaries: "B" ({boundaries_state})', repr(captured.out)

    controller.game.boundaries = not controller.game.boundaries
    controller._show_instructions()
    captured = capsys.readouterr()
    boundaries_state = 'on' if controller.game.boundaries else 'off'
    assert captured.out == f'Exit: "Q", Restart: "R", Toggle boundaries: "B" ({boundaries_state})', repr(captured.out)

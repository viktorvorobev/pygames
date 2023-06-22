import sys

import pytest

import pygames.game_of_life as gof


def test_created():
    instance = gof.GameOfLife()
    assert isinstance(instance, gof.GameOfLife)


def test_created_fail_on_height():
    with pytest.raises(ValueError):
        _ = gof.GameOfLife(height=gof.MIN_SIZE - 1)


def test_created_fail_on_width():
    with pytest.raises(ValueError):
        _ = gof.GameOfLife(width=gof.MIN_SIZE - 1)


def test_game_populated_on_start():
    for _ in range(10):
        game = gof.GameOfLife()
        assert game.population > 0


def test_neighbours_generator():
    game = gof.GameOfLife(height=3, width=3)
    neighbours = []
    for i, j in game._neighbours(1, 1):  # pylint: disable = protected-access
        neighbours.append((i, j))
    assert neighbours == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def test_neighbours_generator_without_boundaries():
    game = gof.GameOfLife(height=3, width=3, boundaries=False)
    neighbours = []
    for i, j in game._neighbours(0, 0, boundaries=False):  # pylint: disable = protected-access
        neighbours.append((i, j))
    assert neighbours == [(2, 2), (2, 0), (2, 1), (0, 2), (0, 1), (1, 2), (1, 0), (1, 1)], neighbours


def test_neighbours_generator_with_boundaries():
    game = gof.GameOfLife(height=3, width=3, boundaries=True)
    neighbours = []
    for i, j in game._neighbours(0, 0, boundaries=True):  # pylint: disable = protected-access
        neighbours.append((i, j))
    assert neighbours == [(sys.maxsize - 1, sys.maxsize - 1), (sys.maxsize - 1, 0), (sys.maxsize - 1, 1),
                          (0, sys.maxsize - 1), (0, 1), (1, sys.maxsize - 1), (1, 0), (1, 1)]


@pytest.mark.parametrize(
    'initial_state',
    [
        [
            [0, 0, 0, ],
            [0, 1, 0, ],
            [0, 0, 0, ],
        ],
        [
            [1, 0, 0, ],
            [0, 1, 0, ],
            [0, 0, 0, ],
        ],
    ]
)
def test_conway_mark_dead_lower_rule(initial_state: list[list[int]]):
    game = gof.GameOfLife(height=3, width=3)
    game.state = initial_state
    game.update()
    assert game.state[1][1] == gof.DEAD, f'Central cell still alive after state {initial_state}'


@pytest.mark.parametrize(
    'initial_state',
    [
        [
            [1, 1, 0, ],
            [0, 1, 0, ],
            [0, 1, 1, ],
        ],
        [
            [1, 1, 0, ],
            [1, 1, 0, ],
            [0, 1, 1, ],
        ],
        [
            [1, 1, 0, ],
            [1, 1, 0, ],
            [1, 1, 1, ],
        ],
        [
            [1, 1, 0, ],
            [1, 1, 1, ],
            [1, 1, 1, ],
        ],
        [
            [1, 1, 1, ],
            [1, 1, 1, ],
            [1, 1, 1, ],
        ],
    ]
)
def test_conway_dead_higher_rule(initial_state: list[list[int]]):
    game = gof.GameOfLife(height=3, width=3)
    game.state = initial_state
    game.update()
    assert game.state[1][1] == gof.DEAD, f'Central cell still alive after state {initial_state}'


@pytest.mark.parametrize(
    'initial_state',
    [
        [
            [1, 0, 0, ],
            [0, 1, 0, ],
            [0, 0, 1, ],
        ],
        [
            [0, 1, 0, ],
            [1, 1, 1, ],
            [0, 0, 0, ],
        ],
    ]
)
def test_still_alive_rule(initial_state: list[list[int]]):
    game = gof.GameOfLife(height=3, width=3)
    game.state = initial_state
    game.update()
    assert game.state[1][1] == gof.LIVE, f'Central cell died after state {initial_state}'


@pytest.mark.parametrize(
    'initial_state',
    [
        [
            [1, 0, 1, ],
            [0, 0, 0, ],
            [0, 0, 1, ],
        ],
        [
            [0, 0, 0, ],
            [1, 0, 1, ],
            [0, 1, 0, ],
        ],
    ]
)
def test_new_cell_rule(initial_state: list[list[int]]):
    game = gof.GameOfLife(height=3, width=3)
    game.state = initial_state
    game.update()
    assert game.state[1][1] == gof.LIVE, f'Central cell not alive after state {initial_state}'


@pytest.mark.parametrize(
    'initial_state,expected,boundaries',
    [
        (
                [
                    [0, 0, 1, ],
                    [0, 0, 1, ],
                    [0, 0, 1, ],
                ],
                1,
                False
        ),
        (
                [
                    [0, 0, 1, ],
                    [0, 0, 1, ],
                    [0, 0, 1, ],
                ],
                0,
                True
        ),
    ]
)
def test_boundaries_set(initial_state: list[list[int]], expected: int, boundaries: bool):
    game = gof.GameOfLife(height=3, width=3, boundaries=boundaries)
    game.state = initial_state
    game.update()
    assert game.state[1][0] == expected, f'Central cell not alive after state {initial_state} {game.state}'

import pytest

from pygames import snake


# pylint: disable = protected-access

def test_created():
    instance = snake.Snake()
    assert isinstance(instance, snake.Snake)


@pytest.mark.parametrize(
    'initial_state,direction,expected_state',
    [
        (
                [[1, 1]],
                snake.Direction.LEFT,
                [[0, 1]]
        ),
        (
                [[1, 1]],
                snake.Direction.RIGHT,
                [[2, 1]]
        ),
        (
                [[1, 1]],
                snake.Direction.UP,
                [[1, 0]]
        ),
        (
                [[1, 1]],
                snake.Direction.DOWN,
                [[1, 2]]
        ),
    ]
)
def test_snake_move(initial_state: list[list[int]], direction: snake.Direction, expected_state: list[list[int]]):
    game = snake.Snake(width=3, height=3)
    game.fruit = [-1, -1]
    game._direction = direction
    game.snake = initial_state
    game.update()
    assert game.snake == expected_state


@pytest.mark.parametrize('initial_direction,forbidden_direction', [
    (snake.Direction.UP, snake.Direction.DOWN),
    (snake.Direction.DOWN, snake.Direction.UP),
    (snake.Direction.RIGHT, snake.Direction.LEFT),
    (snake.Direction.LEFT, snake.Direction.RIGHT),
])
def test_snake_change_direction(initial_direction, forbidden_direction):
    game = snake.Snake(width=3, height=3)
    game.fruit = [-1, -1]
    for new_direction in list(snake.Direction):
        game._direction = initial_direction
        game.direction = new_direction
        assert game.direction == new_direction if new_direction != forbidden_direction else initial_direction


@pytest.mark.parametrize('direction', list(snake.Direction))
def test_snake_crash(direction: snake.Direction):
    game = snake.Snake(width=3, height=3, boundaries=True)
    game.fruit = [-1, -1]
    game._direction = direction
    game.snake = [[1, 1]]
    game.update()
    with pytest.raises(snake.GameOverException):
        game.update()


@pytest.mark.parametrize(
    'initial_state,direction,expected_state',
    [
        (
                [[1, 1]],
                snake.Direction.LEFT,
                [[2, 1]]
        ),
        (
                [[1, 1]],
                snake.Direction.RIGHT,
                [[0, 1]]
        ),
        (
                [[1, 1]],
                snake.Direction.UP,
                [[1, 2]]
        ),
        (
                [[1, 1]],
                snake.Direction.DOWN,
                [[1, 0]]
        ),
    ]
)
def test_snake_move_no_boundaries(
        initial_state: list[list[int]], direction: snake.Direction, expected_state: list[list[int]]
):
    game = snake.Snake(width=3, height=3)
    game.fruit = [-1, -1]
    game._direction = direction
    game.snake = initial_state
    game.update()
    game.update()
    assert game.snake == expected_state


@pytest.mark.parametrize(
    'initial_state,direction,expected_state',
    [
        (
                [[2, 1], [2, 2]],
                snake.Direction.LEFT,
                [[1, 1], [2, 1]]
        ),
        (
                [[2, 1], [2, 2]],
                snake.Direction.RIGHT,
                [[3, 1], [2, 1]]
        ),
        (
                [[2, 1], [2, 2]],
                snake.Direction.UP,
                [[2, 0], [2, 1]]
        ),
    ]
)
def test_long_snake_move(initial_state: list[list[int]], direction: snake.Direction, expected_state: list[list[int]]):
    game = snake.Snake(width=5, height=5)
    game.fruit = [-1, -1]
    game._direction = direction
    game.snake = initial_state
    game.update()
    assert game.snake == expected_state


@pytest.mark.parametrize(
    'initial_state,direction',
    [
        (
                [[2, 1], [2, 2], [2, 3]],
                snake.Direction.DOWN,
        ),
        (
                [[1, 2], [1, 1], [2, 1], [2, 2], [2, 3]],
                snake.Direction.RIGHT,
        ),
    ]
)
def test_body_collision(initial_state: list[list[int]], direction: snake.Direction):
    game = snake.Snake(width=5, height=5)
    game.fruit = [-1, -1]
    game._direction = direction
    game.snake = initial_state
    with pytest.raises(snake.GameOverException):
        game.update()


def test_fruit_added():
    game = snake.Snake()
    assert game.fruit != [-1, -1]
    assert game.fruit not in game.snake
    assert 0 <= game.fruit[0] < game.width
    assert 0 <= game.fruit[1] < game.height


@pytest.mark.parametrize(
    'initial_state,fruit_position,direction,expected_state',
    [
        (
                [[1, 1]],
                [0, 1],
                snake.Direction.LEFT,
                [[0, 1], [1, 1]]
        ),
        (
                [[1, 1]],
                [1, 0],
                snake.Direction.UP,
                [[1, 0], [1, 1]]
        ),
        (
                [[1, 1]],
                [2, 1],
                snake.Direction.RIGHT,
                [[2, 1], [1, 1]]
        ),
    ]
)
def test_fruit_eaten(
        initial_state: list[list[int]], fruit_position: list[int],
        direction: snake.Direction, expected_state: list[list[int]]
):
    game = snake.Snake(width=3, height=3)
    game.snake = initial_state
    game.fruit = fruit_position
    game._direction = direction
    assert game.score == 0

    game.update()
    assert game.score == game.SCORE_INC
    assert game.snake == expected_state


def test_game_over():
    game = snake.Snake(width=3, height=3)
    game._direction = snake.Direction.UP
    game.fruit = [0, 0]
    game.snake = [[0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0], [1, 1]]

    with pytest.raises(snake.GameOverException):
        game.update()


def test_game_reset():
    width, height = 5, 3
    game = snake.Snake(width=5, height=3)
    game._direction = snake.Direction.UP
    game.fruit = [0, 0]
    game.snake = [[0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0], [1, 1]]
    game.score = 10

    game.reset_state()
    assert game.snake == [[width // 2, height // 2]]
    assert game.score == 0

import enum

import random


class GameOverException(Exception):
    pass


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Snake:  # pylint: disable = too-few-public-methods, too-many-instance-attributes
    SCORE_INC = 1

    def __init__(self, height: int = 10, width: int = 10, boundaries: bool = False):
        self.height = height
        self.width = width
        self.boundaries = boundaries
        self.snake: list[list[int]] = [[self.width // 2, self.height // 2]]
        self._direction: Direction = Direction.RIGHT
        self.score = 0
        self.fruit: list[int] = [-1, -1]
        self._set_fruit()

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        # forbid in-place direction swap
        # pylint: disable = too-many-boolean-expressions
        if (new_direction == Direction.UP and self._direction == Direction.DOWN) \
                or (new_direction == Direction.DOWN and self._direction == Direction.UP) \
                or (new_direction == Direction.RIGHT and self._direction == Direction.LEFT) \
                or (new_direction == Direction.LEFT and self._direction == Direction.RIGHT):
            return
        self._direction = new_direction

    def _set_fruit(self):
        if len(self.snake) == self.height * self.width:
            raise GameOverException('Nowhere to place fruit')
        while not self.__fruit_valid:
            self.fruit = [random.randint(0, self.width), random.randint(0, self.height)]

    @property
    def __fruit_valid(self):
        fruit_in_bound = 0 <= self.fruit[0] < self.width and 0 <= self.fruit[1] < self.height
        return self.fruit not in self.snake and fruit_in_bound

    def reset_state(self):
        self.score = 0
        self.snake = [[self.width // 2, self.height // 2]]
        self._set_fruit()
        self._direction = Direction.RIGHT

    def update(self):
        self._move()
        self._check_body_collision()
        self._check_fruit_eaten()

    def _check_fruit_eaten(self):
        head = self.snake[0]
        if self.fruit == head:
            self.score += self.SCORE_INC
            self._set_fruit()
        else:
            self.snake.pop(-1)

    def _move(self):
        head_x, head_y = self.snake[0]
        new_head_x = new_head_y = 0

        match self.direction:
            case Direction.UP:
                new_head_x, new_head_y = head_x, head_y - 1
            case Direction.DOWN:
                new_head_x, new_head_y = head_x, head_y + 1
            case Direction.RIGHT:
                new_head_x, new_head_y = head_x + 1, head_y
            case Direction.LEFT:
                new_head_x, new_head_y = head_x - 1, head_y

        if self.boundaries:
            if new_head_x < 0 or new_head_x >= self.width or new_head_y < 0 or new_head_y >= self.height:
                raise GameOverException('Wall hit')

        if new_head_x < 0:
            new_head_x = self.width - 1
        if new_head_x >= self.width:
            new_head_x = 0
        if new_head_y < 0:
            new_head_y = self.height - 1
        if new_head_y >= self.height:
            new_head_y = 0

        self.snake.insert(0, [new_head_x, new_head_y])

    def _check_body_collision(self):
        if self.snake[0] in self.snake[1:]:
            raise GameOverException('Body hit')

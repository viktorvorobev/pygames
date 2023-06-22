import copy
import random
import sys
import typing as t

DEAD = 0
LIVE = 1
MIN_SIZE = 3


class GameOfLife:

    def __init__(self, height: int = 10, width: int = 10, boundaries: bool = False):
        if height < MIN_SIZE:
            raise ValueError(f'Height of size {height} is too small. Minimal value is {MIN_SIZE}')
        if width < MIN_SIZE:
            raise ValueError(f'Width of size {width} is too small. Minimal value is {MIN_SIZE}')
        self._boundaries = boundaries
        self._height = height
        self._width = width
        self.state: list[list[int]] = [[]]
        while not self.population:
            self.reset_state()

    def reset_state(self):
        self.state = [
            random.choices(
                population=(DEAD, LIVE),
                weights=(0.8, 0.2),
                k=self._width
            ) for _ in range(self._height)
        ]

    def update(self):
        new_state = copy.deepcopy(self.state)
        for row in range(self._height):
            for col in range(self._width):
                total = sum(
                    self.state[drow][dcol]
                    for drow, dcol in self._neighbours(row, col, self._boundaries)
                    if 0 <= drow <= self._height - 1
                    and 0 <= dcol <= self._width - 1
                )

                if self.state[row][col] == LIVE:
                    if (total < 2) or (total > 3):
                        new_state[row][col] = DEAD
                else:
                    if total == 3:
                        new_state[row][col] = LIVE
        self.state = copy.deepcopy(new_state)

    def _neighbours(self, row: int, col: int, boundaries: bool = True) -> t.Generator[tuple[int, int], None, None]:
        height_boundary = sys.maxsize if boundaries else self._height
        width_boundary = sys.maxsize if boundaries else self._width

        yield (row - 1) % height_boundary, (col - 1) % width_boundary
        yield (row - 1) % height_boundary, col % width_boundary
        yield (row - 1) % height_boundary, (col + 1) % width_boundary
        yield row % height_boundary, (col - 1) % width_boundary
        yield row % height_boundary, (col + 1) % width_boundary
        yield (row + 1) % height_boundary, (col - 1) % width_boundary
        yield (row + 1) % height_boundary, col % width_boundary
        yield (row + 1) % height_boundary, (col + 1) % width_boundary

    @property
    def population(self):
        return sum(sum(cell for cell in row if cell == LIVE) for row in self.state)

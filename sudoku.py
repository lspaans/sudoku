#!/usr/bin/env python

import random
import re

SUDOKU_EXAMPLE = """
    ......68.
    ....73..9
    3.9....45
    49.......
    8.3.5.9.2
    .......36
    96....3.8
    7..68....
    .28......
"""
SUDOKU_BASE    = 9

class Game(object):
    def __init__(self, *args, **kwargs):
        self._finished = False
        self._turn     = 0

    def _do_turn(self):
        self._turn += 1
        if random.choice((True, False)):
            self._finished = True

    def start(self):
        while not(self._finished):
            self._do_turn()

class Sudoku(Game):
    def __init__(
        self, base=SUDOKU_BASE, grid=SUDOKU_EXAMPLE, *args, **kwargs
    ):
        super(Sudoku, self).__init__(*args, **kwargs)
        self._base = base
        self._init_grid(grid)

    def _do_turn(self):
        super(Sudoku, self)._do_turn()
        print('{0}\n'.format(self))

    def _init_grid(self, grid):
        self._grid    = []
        self._columns = map(lambda n: [], xrange(self._base))
        self._rows    = map(lambda n: [], xrange(self._base))
        self._boxes   = map(lambda n: [], xrange(self._base))
        for n, value in enumerate(
            filter(lambda v: re.match(r'[\d\.]', v), grid)
        ):
            cell = Cell(value)
            self._grid.append(cell)
            self._columns[n%self._base].append(cell)
            self._rows[n/self._base].append(cell)
            self._boxes[
                int(self._base**0.5)*((n/self._base)/int(self._base**0.5)) +
                (n%self._base)/int(self._base**0.5)
            ].append(cell)

    def __str__(self):
        return('\n'.join(map(lambda n: ''.join(
            map(lambda cell: str(cell), self._rows[n])), xrange(self._base))
        ))


class Cell(object):
    def __init__(self, value, min=1, max=SUDOKU_BASE):
        self._min = min
        self._max = max
        self.set_value(value)

    def _valid_value(self, value):
        return(value is None or (
            value.isdigit() and
            self._min <= int(value) <= self._max
        ))

    def get_value(self):
        return(self._value)

    def set_value(self, value=None):
        if value == '.':
            value = None
        if self._valid_value(value):
            self._value = value
        else:
            raise(ValueError(
                'Value is not a digit [{0}..{1}]: "{2}"'.format(
                    self._min, self._max, value
            )))

    def __str__(self):
        value = self.get_value()
        if value is None:
            value = ' '
        return('[{0}]'.format(value))

def main():
    Sudoku().start()

if __name__ == '__main__':
    main()

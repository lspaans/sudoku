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
    def __init__(self, grid=SUDOKU_EXAMPLE, *args, **kwargs):
        super(Sudoku, self).__init__(*args, **kwargs)
        self._init_grid(grid)

    def _do_turn(self):
        super(Sudoku, self)._do_turn()

    def _init_grid(self, grid):
        self._columns = map(lambda n: [], xrange(9))
        self._rows    = map(lambda n: [], xrange(9))
        self._boxes   = map(lambda n: [], xrange(9))
        for n, value in enumerate(
            filter(lambda v: re.match(r'[\d\.]', v), grid)
        ):
            cell = Cell(value)
            self._columns[n%9].append(cell)
            self._rows[n/9].append(cell)
            self._boxes[3*((n/9)/3) + (n%9)/3].append(cell)

    def __str__(self):
        return('\n'.join(map(lambda n: ''.join(
            map(lambda cell: str(cell), self._rows[n])), xrange(9))
        ))


class Cell(object):
    def __init__(self, value):
        self.set_value(value)

    def _valid_value(self, value):
        return(value is None or (
            value.isdigit() and
            1 <= int(value) <= 9
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
                'Value is not a digit [1..9]: "{0}"'.format(value)
            ))

    def __str__(self):
        value = self.get_value()
        if value is None:
            value = ' '
        return('[{0}]'.format(value))

def main():
    sudoku = Sudoku()
    print(sudoku)
    sudoku.start()

if __name__ == '__main__':
    main()

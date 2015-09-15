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
        self._find_values_for_grid_positions()
        self._find_cell_positions_for_values()

    def _find_cell_positions_for_values(self):
        for n in xrange(len(self._boxes)):
            free_values = set(xrange(1, self._base+1)) - self._get_box_values(n)
            for pos in self._get_free_box_positions(n):
                possible_values = self._get_possible_box_cell_values(n, pos)
                values = free_values.intersection(possible_values)
                if len(values) == 1:
                    self._boxes[n][pos].set_value(str(values.pop()))
            print('box[{0}]: ({1})'.format(n, repr(values)))
        for n in xrange(len(self._columns)):
            free_values = set(xrange(1, self._base+1)) - self._get_column_values(n)
            for pos in self._get_free_column_positions(n):
                possible_values = self._get_possible_column_cell_values(n, pos)
                values = free_values.intersection(possible_values)
                if len(values) == 1:
                    self._columns[n][pos].set_value(str(values.pop()))
            print('column[{0}]: ({1})'.format(n, repr(values)))
        for n in xrange(len(self._rows)):
            free_values = set(xrange(1, self._base+1)) - self._get_row_values(n)
            for pos in self._get_free_row_positions(n):
                possible_values = self._get_possible_row_cell_values(n, pos)
                values = free_values.intersection(possible_values)
                if len(values) == 1:
                    self._rows[n][pos].set_value(str(values.pop()))
            print('row[{0}]: ({1})'.format(n, repr(values)))

    def _find_values_for_grid_positions(self):
        for n in self._get_free_grid_positions():
            possible_cell_values = self._get_possible_cell_values(n)
            if len(possible_cell_values) == 1:
                self._grid[n].set_value(str(possible_cell_values.pop()))

    def _get_box_values(self, n):
        return(self._get_values(self._boxes[n]))

    def _get_box_number(self, c):
        return(((c/self._base)/3)*3 + (c%self._base)/3)

    def _get_column_values(self, n):
        return(self._get_values(self._columns[n]))

    def _get_column_number(self, c):
        return(c%self._base)

    def _get_free_box_positions(self, n):
        return(self._get_free_positions(self._boxes[n]))

    def _get_free_column_positions(self, n):
        return(self._get_free_positions(self._columns[n]))

    def _get_free_row_positions(self, n):
        return(self._get_free_positions(self._rows[n]))

    def _get_free_grid_positions(self):
        return(self._get_free_positions(self._grid))
        
    def _get_free_positions(self, cells):
        return(filter(
            lambda n: cells[n].get_value() == 0,
                xrange(len(cells))
        ))

    def _get_row_values(self, n):
        return(self._get_values(self._rows[n]))

    def _get_row_number(self, c):
        return(c/self._base)

    def _get_possible_box_cell_values(self, box, n):
# HIERO
#        return(self._get_possible_cell_values(0))
        return(set())

    def _get_possible_column_cell_values(self, column, n):
        return(self._get_possible_cell_values(self._base*column + n))

    def _get_possible_row_cell_values(self, row, n):
        return(self._get_possible_cell_values(self._base*row + n))

    def _get_possible_cell_values(self, n):
        return(set(xrange(1, self._base+1)) - set(
            map(lambda cell: cell.get_value(), (
                self._boxes[self._get_box_number(n)] +
                self._columns[self._get_column_number(n)] +
                self._rows[self._get_row_number(n)]
        ))))

    def _get_values(self, cells):
        return(set(map(lambda cell: cell.get_value(),
            filter(lambda cell: cell.get_value() != 0, cells)
        )))

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
            self._columns[self._get_column_number(n)].append(cell)
            self._rows[self._get_row_number(n)].append(cell)
            self._boxes[self._get_box_number(n)].append(cell)

    def __str__(self):
        return('\n'.join(map(lambda n: ''.join(
            map(lambda cell: str(cell), self._rows[n])), xrange(self._base))
        ))

class Cell(object):
    def __init__(self, value, min=0, max=SUDOKU_BASE):
        self._min = min
        self._max = max
        self.set_value(value)

    def _valid_value(self, value):
        return(value.isdigit() and self._min <= int(value) <= self._max)

    def get_value(self):
        return(self._value)

    def set_value(self, value=0):
        if value == '.':
            value = "0"
        if self._valid_value(value):
            self._value = int(value)
        else:
            raise(ValueError((
                'Value is not a number or not in range ' +
                '[{0}..{1}]: "{2}"').format(
                    self._min, self._max, value
            )))

    def __str__(self):
        value = self.get_value()
        if value == 0:
            value = ' '
        return('[{0}]'.format(value))

def main():
    Sudoku().start()

if __name__ == '__main__':
    main()

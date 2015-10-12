#!/usr/bin/env python

import math
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
SUDOKU_BASE = 9


class Game(object):
    def __init__(self, *args, **kwargs):
        self._finished = False
        self._turn = 0

    def _do_turn(self):
        if self._finished:
            self._do_finish()
        self._turn += 1

    def _do_finish(self):
        sys.exit(0)

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

    def _do_display(self):
        print('{0}\n'.format(self))

    def _do_turn(self):
        super(Sudoku, self)._do_turn()
        self._do_display()
        self._find_values_for_grid_positions()
        self._find_cell_positions_for_values()
        if len(self._get_free_grid_positions()) == 0:
            self._finished = True

    def _find_cell_positions_for_values(self):
        for n in xrange(len(self._boxes)):
            free_values = (
                set(xrange(1, self._base+1)) - self._get_box_values(n)
            )
            for pos in self._get_free_box_positions(n):
                possible_values = self._get_possible_box_cell_values(n, pos)
                values = free_values.intersection(possible_values)
                print((
                    'box={0}, pos=({1}), free_values=({2}), ' +
                    'possible_values=({3}), values=({4})'
                    ).format(n, pos, free_values, possible_values, values)
                )
                if len(values) == 1:
                    value = values.pop()
                    self._boxes[n][pos].set_value(str(value))
                    free_values.remove(value)
                    self._do_display()
        for n in xrange(len(self._columns)):
            free_values = (
                set(xrange(1, self._base+1)) - self._get_column_values(n)
            )
            for pos in self._get_free_column_positions(n):
                possible_values = self._get_possible_column_cell_values(n, pos)
                values = free_values.intersection(possible_values)
                print((
                    'column={0}, pos=({1}), free_values=({2}), ' +
                    'possible_values=({3}), values=({4})'
                    ).format(n, pos, free_values, possible_values, values)
                )
                if len(values) == 1:
                    value = values.pop()
                    self._columns[n][pos].set_value(str(value))
                    free_values.remove(value)
                    self._do_display()
        for n in xrange(len(self._rows)):
            free_values = (
                set(xrange(1, self._base+1)) - self._get_row_values(n)
            )
            for pos in self._get_free_row_positions(n):
                possible_values = self._get_possible_row_cell_values(n, pos)
                values = free_values.intersection(possible_values)
                print((
                    'row={0}, pos=({1}), free_values=({2}), ' +
                    'possible_values=({3}), values=({4})'
                    ).format(n, pos, free_values, possible_values, values)
                )
                if len(values) == 1:
                    value = values.pop()
                    self._rows[n][pos].set_value(str(value))
                    free_values.remove(value)
                    self._do_display()

    def _find_values_for_grid_positions(self):
        for n in self._get_free_grid_positions():
            possible_cell_values = self._get_possible_cell_values(n)
            if len(possible_cell_values) == 1:
                self._grid[n].set_value(str(possible_cell_values.pop()))
                self._do_display()

    def _get_box_values(self, n):
        return(self._get_values(self._boxes[n]))

    def _get_box_number(self, c):
        return(((c/self._base)/3)*3 + (c % self._base)/3)

    def _get_column_values(self, n):
        return(self._get_values(self._columns[n]))

    def _get_column_number(self, c):
        return(c % self._base)

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
            lambda n: cells[n].get_value() == 0, xrange(len(cells))
        ))

    def _get_row_values(self, n):
        return(self._get_values(self._rows[n]))

    def _get_row_number(self, c):
        return(c/self._base)

    def _get_possible_box_cell_values(self, box, n):
        print((
            '_get_possible_box_cell_values(<..>): ' +
            'box={0}, n={1}, grid_pos= {2}').format(
                box, n,
                self._base * (
                    int(box // math.sqrt(self._base) * math.sqrt(self._base)) +
                    int(n // math.sqrt(self._base))
                ) +
                int(box % math.sqrt(self._base) * math.sqrt(self._base)) +
                int(n % math.sqrt(self._base))
        ))
        return(self._get_possible_cell_values(
            self._base * (
                int(box // math.sqrt(self._base) * math.sqrt(self._base)) +
                int(n // math.sqrt(self._base))
            ) +
            int(box % math.sqrt(self._base) * math.sqrt(self._base)) +
            int(n % math.sqrt(self._base))
        ))

    def _get_possible_column_cell_values(self, column, n):
        return(self._get_possible_cell_values(self._base*n + column))

    def _get_possible_row_cell_values(self, row, n):
        return(self._get_possible_cell_values(self._base*row + n))

    def _get_possible_cell_values(self, n):
        return((
            set(xrange(1, self._base+1)) - set(
                map(lambda cell: cell.get_value(), (
                    self._boxes[self._get_box_number(n)] +
                    self._columns[self._get_column_number(n)] +
                    self._rows[self._get_row_number(n)]
                ))
            )
        ))

    def _get_values(self, cells):
        return(set(
            map(lambda cell: cell.get_value(), filter(
                lambda cell: cell.get_value() != 0, cells
            ))
        ))

    def _init_grid(self, grid):
        self._grid = []
        self._columns = map(lambda n: [], xrange(self._base))
        self._rows = map(lambda n: [], xrange(self._base))
        self._boxes = map(lambda n: [], xrange(self._base))
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


class SetMap(object):
    def __init__(self, keys=(), values=()):
        self._keys = set()
        self._values = set()
        self.add_keys(keys)
        self.add_values(values)

    def get_keys(self):
        return(self._keys)

    def get_values(self):
        return(self._values)

    def add_keys(self, keys):
        if self._valid_keys(keys):
            self._keys.update(keys)
        else:
            raise(ValueError('Invalid "keys"-argument'))

    def delete_keys(self, keys):
        deletes = 0
        if self._valid_keys(keys):
            deletes = len(self._keys.intersection(keys))
            self._keys = self._keys - keys
            return(deletes)
        else:
            raise(ValueError('Invalid "keys"-argument'))

    def delete_values(self, values):
        deletes = 0
        if self._valid_values(values):
            deletes = len(self._values.intersection(values))
            self._values = self._values - values
            return(deletes)
        else:
            raise(ValueError('Invalid "values"-argument'))

    def add_values(self, values):
        if self._valid_values(values):
            self._values.update(values)
        else:
            raise(ValueError('Invalid "values"-argument'))

    def has_keys(self, keys):
        return(self.get_keys().issuperset(keys))

    def has_values(self, values):
        return(self.get_values().issuperset(values))

    def matches_keys(self, keys):
        return(self.get_keys() == set(keys))

    def matches_values(self, values):
        return(self.get_values() == set(values))

    def _valid_keys(self, keys):
        if (
            not isinstance(keys, (list, set, tuple)) or
            len(filter(lambda o: not(isinstance(o, (str, int))), keys)) > 0 or
            len(keys) == 0
        ):
            return(False)
        return(True)

    def _valid_values(self, values):
        if (
            not isinstance(values, (list, set, tuple)) or
            len(filter(lambda o: not(isinstance(o, (str, int))), values)) > 0
        ):
            return(False)
        return(True)

    def __str__(self):
        return('({0}) = ({1})'.format(
            ', '.join(map(lambda s: str(s), self.get_keys())),
            ', '.join(map(lambda s: str(s), self.get_values()))
        ))

    def __repr__(self):
        return(self.__str__())


class SetMapSet(object):
    def __init__(self, values=()):
        self.set_values(values)

    def add_values(self, values):
        if self._valid_values(values):
            if isinstance(values, SetMap):
                self._append_value(values)
            else:
                for value in values:
                    self.add_values(value)
        else:
            raise(ValueError('Invalid "values"-argument'))

    def get_values(self):
        return(self._values)

    def set_values(self, values=()):
        self._values = []
        self.add_values(values)

    def _append_value(self, sh):
        merged = False
        for n in xrange(len(self._values)):
            if self._values[n].matches_values(sh.get_values()):
                self._values[n].add_keys(sh.get_keys())
                merged = True
        if merged is False:
            self._values.append(sh)
        self._simplify()

    def _simplify(self):
        changes = True
        while changes is True:
            changes = False
            for a in self.get_values():
                if len(a.get_values()) != len(a.get_keys()):
                    continue
                for b in self.get_values():
                    if a.matches_keys(b.get_keys()):
                        continue
                    if b.delete_values(a.get_values()) > 0:
                        changes = True

    def _valid_values(self, values):
        if (
            isinstance(values, (list, tuple)) and
            len(filter(lambda o: not(isinstance(o, SetMap)), values)) == 0
        ) or isinstance(values, SetMap):
            return(True)
        return(False)

    def __str__(self):
        return('\n'.join(map(str, self.get_values())))

    def __repr__(self):
        return(self.__str__())


def main():
    Sudoku().start()

if __name__ == '__main__':
    main()

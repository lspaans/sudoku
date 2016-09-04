#!/usr/bin/env python

import math

from cell import Cell, CellGroup
from solution import Solution, SolutionSet

class CellSet(CellGroup):

    MAXIMUM = 9
    NEWLINE_POSITION = MAXIMUM
    UNIQUE = True

    def has_value(self, value):
        for cell in self.cells:
            if cell.value == value:
                return(True)
        return(False)


    def get_value_position(self, value):
        for position, cell in enumerate(self.cells):
            if cell.value == value:
                return(position)

        raise ValueError("Value {value} does not exist in {type}".format(
            value=value,
            type=type(self)
        ))


class Column(CellSet):

    SEPARATOR = "\n"


class Row(CellSet):

    pass


class Tile(CellSet):

    NEWLINE_POSITION = int(round(math.sqrt(CellSet.MAXIMUM)))


class Board(object):

    def __init__(self, line):
        self._columns = map(lambda n: Column([]), xrange(Column.MAXIMUM))
        self._rows = map(lambda n: Row([]), xrange(Row.MAXIMUM))
        self._tiles = map(lambda n: Tile([]), xrange(Tile.MAXIMUM))
        cells = []
        for c in line:
            if (
                c.isdigit() and
                int(c) - 1 in xrange(CellSet.MAXIMUM)
            ):
                cells.append(Cell(int(c)))
            else:
                cells.append(Cell(0))
        self.cells = cells[:CellSet.MAXIMUM**2]


    @property
    def cells(self):
        return(self._cells)


    @property
    def columns(self):
        return(self._columns)


    @property
    def rows(self):
        return(self._rows)


    @property
    def tiles(self):
        return(self._tiles)


    @cells.setter
    def cells(self, cells):
        if self._is_valid_input(cells):
            self._cells = []
            for (position, cell) in enumerate(cells[:CellSet.MAXIMUM**2]):
                self._cells.append(cell)
                self._columns[self.get_column(position)].add(cell)
                self._rows[self.get_row(position)].add(cell)
                self._tiles[self.get_tile(position)].add(cell)
        else:
            raise ValueError("Cannot initialize cells")

    def get_column(self, position):
        return(position%Column.MAXIMUM)

    def get_row(self, position):
        return(position//Row.MAXIMUM)

    def get_tile(self, position):
        return(int((
                (position // math.sqrt(Tile.MAXIMUM) ** 3) *
                math.sqrt(Tile.MAXIMUM)
            ) +
            (position % Tile.MAXIMUM) // math.sqrt(Tile.MAXIMUM)
        ))

    def _is_valid_input(self, values):
        return(
            isinstance(values, (list, tuple)) and
            len(values) == CellSet.MAXIMUM**2 and
            len(filter(lambda v: isinstance(v, Cell), values)) == len(values)
        )


    def __str__(self):
        return("\n".join(map(lambda r: str(r), self.rows)))


    def __repr__(self):
        return(self.__str__())

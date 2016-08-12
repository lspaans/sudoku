#!/usr/bin/env python

import math

from cell import Cell, CellGroup
from solution import Solution, SolutionSet

class CellSet(CellGroup):

    MAXIMUM = 9
    NEWLINE_POSITION = MAXIMUM
    UNIQUE = True


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
            for (n, cell) in enumerate(cells[:CellSet.MAXIMUM**2]):
                self._cells.append(cell)
                self._columns[self._get_cell_column(n)].add(cell)
                self._rows[self._get_cell_row(n)].add(cell)
                self._tiles[self._get_cell_tile(n)].add(cell)
        else:
            raise ValueError("Cannot initialize cells")

    def _get_cell_column(self, n):
        return(n%Column.MAXIMUM)

    def _get_cell_row(self, n):
        return(n//Row.MAXIMUM)

    def _get_cell_tile(self, n):
        return(int(
            (n // math.sqrt(Tile.MAXIMUM) ** 3) * math.sqrt(Tile.MAXIMUM) +
            (n % Tile.MAXIMUM) // math.sqrt(Tile.MAXIMUM)
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

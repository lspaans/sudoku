#!/usr/bin/env python

import os
import sys

DEF_TILE_BASE = 3

class Cell(object):
    def __init__(self, value=None, tileBase=DEF_TILE_BASE, options=[]):
        self._tileBase = tileBase
        self.maxValue = self._tileBase ** 2
        self.allOptions = range(1, self.maxValue + 1)
        self.options = self.allOptions
        self.value = value

    @property
    def maxValue(self):
        return self._maxValue

    @property
    def options(self):
        return tuple(self._options)

    @property
    def value(self):
        return self._value

    @property
    def col(self):
        return self._col

    @property
    def col_n(self):
        return self._col_n

    @property
    def row(self):
        return self._row

    @property
    def row_n(self):
        return self._row_n

    @property
    def tile(self):
        return self._tile

    @property
    def tile_n(self):
        return self._tile_n

    @maxValue.setter
    def maxValue(self, maxValue):
        self._maxValue = maxValue

    @options.setter
    def options(self, options=[]):
        self._options = set(options)

    def delOptions(self, options=[]):
       self.options = tuple(set(self.options) - set(options))

    @value.setter
    def value(self, value=None):
        if value in self.options:
            self._value, self.options = value, []
        elif value is None or value == 0:
            self._value = None 
            self.options = self.allOptions
        else:
            raise ValueError("Invalid value ({0})".format(value))

    @col.setter
    def col(self, col):
        if isinstance(type(col), type(Col)):
            self._col = col
        else:
            raise ValueError("Non Col()-class ({0})".format(type(col)))

    @col_n.setter
    def col_n(self, col_n):
        self._col_n = col_n

    @row.setter
    def row(self, row):
        if isinstance(type(row), type(Row)):
            self._row = row
        else:
            raise ValueError("Non Row()-class ({0})".format(type(row)))

    @row_n.setter
    def row_n(self, row_n):
        self._row_n = row_n

    @tile.setter
    def tile(self, tile):
        if isinstance(type(tile), type(Tile)):
            self._tile = tile
        else:
            raise ValueError("Non Tile()-class ({0})".format(type(tile)))

    @tile_n.setter
    def tile_n(self, tile_n):
        self._tile_n = tile_n

    def __str__(self):
        if self._value is None:
            return "[ ]"
        else:
            return "[{0}]".format(self._value)

    def __repr__(self):
        return self.__str__()

class CellGroup(object):
    def __init__(self, maxCells=DEF_TILE_BASE ** 2, tileBase=DEF_TILE_BASE):
        self._maxCells = maxCells
        self._tileBase = tileBase
        self._cells = []

### HIERO

        self._options = []
        self._positions = []

### HIERO

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, cells=[]):
        for cell in cells:
            self.addCell(cell)

# HIERO CONTROLEREN OF VALUE VAN CELL UNIQUE IS

    def addCell(self, cell):
        if self._maxCells <= len(self._cells):
            raise ValueError("Too many cells")
        self._cells.append(cell)

class Col(CellGroup):
    def __str__(self):
        return "\n".join(map(lambda c: str(c), self.cells))

    def __repr__(self):
        return self.__str__()

class Row(CellGroup):
    def __str__(self):
        return " ".join(map(lambda c: str(c), self.cells))

    def __repr__(self):
        return self.__str__()

class Tile(CellGroup):
    def __str__(self):
        out = ""
        for y in xrange(self._tileBase):
            s = y * self._tileBase
            e = s + self._tileBase
            out += "{0}\n".format(
                " ".join(map(lambda c: str(c), self.cells[s:e]))
            )
        return out

    def __repr__(self):
        return self.__str__()

class Board(object):
    def __init__(self, valueStr=None, tileBase=DEF_TILE_BASE):
        self._tileBase = tileBase
        self._cells = CellGroup(self._tileBase ** 4)
        self._col_map = {}
        self._row_map = {}
        self._tile_map = {}
        self._cols = []
        self._rows = []
        self._tiles = []
        self.initCells(valueStr)
        self.initCellGroups()
        self.updateCells()

    def initCells(self, valueStr=None):
        for n in xrange(self._tileBase ** 4):
            c = Cell(None)
            if not valueStr is None and len(valueStr) > 0:
                value, valueStr = valueStr[0:1:], valueStr[1::]
                c.value = int(value)
            self._row_map[n], self._col_map[n] = divmod(n, self._tileBase ** 2)
            c.row_n, c.col_n = divmod(n, self._tileBase ** 2)
            c.tile_n = (
                self._tileBase * (n // self._tileBase ** self._tileBase) +
                (n % self._tileBase ** 2) // self._tileBase
            )
            self._tile_map[n] = (
                self._tileBase * (n // self._tileBase ** self._tileBase) +
                (n % self._tileBase ** 2) // self._tileBase
            )
            self.cells.addCell(c)

    def initCellGroups(self):
        for n in xrange(self._tileBase ** 2):
            col = Col()
            row = Row()
            tile = Tile()
            for c in self._cells.cells:
                if c.col_n == n:
                    col.addCell(c)
                if c.row_n == n:
                    row.addCell(c)
                if c.tile_n == n:
                    tile.addCell(c)
            self.cols.append(col)
            self.rows.append(row)
            self.tiles.append(tile)

    def updateCells(self):
        for n in xrange(self._tileBase ** 4):
            c = self.cells.cells[n]
            c.col = self.cols[c.col_n]
            c.row = self.rows[c.row_n]
            c.tile = self.tiles[c.tile_n]

    @property
    def cell(self, cell):
        if cell >= len(self._cells):
            raise ValueError("Invalid cell")
        return self._cells[cell]

    @property
    def cells(self):
        return self._cells

    def col(self, col):
        if col >= self._tileBase ** 2:
            raise ValueError("Invalid col")
        return self._cols[col]

    @property
    def cols(self):
        return self._cols

    def row(self, row):
        if row >= self._tileBase ** 2:
            raise ValueError("Invalid row")
        return self._rows[row]

    @property
    def rows(self):
        return self._rows

    def tile(self, tile):
        if tile >= self._tileBase ** 2:
            raise ValueError("Invalid tile")
        return self._tiles[tile]

    @property
    def tiles(self):
        return self._tiles

    def __str__(self):
        out = "\n".join(map(lambda r: str(r), self._rows))
        return out

    def __repr__(self):
        return self.__str__()

class Game(object):
    def __init__(self, tileBase=DEF_TILE_BASE):
        self._board = Board()

if __name__ == '__main__':
    boards = [
        "02900170080000030600700000410000500060002" + 
            "3009900008000004000003500000402013002500",
        "10000276020000100803600700400006087260702" + 
            "9000000000000080070300013000500000010097",
        "00004070000000105084000200310050003060900" + 
            "7000500100020780005001000006040000030200"
    ]
    os.system('clear')
    b = Board(boards[1])
    print(str(b))
    print("")
    print(str(b.cells.cells[0].col))
    print("")
    print(str(b.cells.cells[0].row))
    print("")
    print(str(b.cells.cells[0].tile))
    sys.exit(0)

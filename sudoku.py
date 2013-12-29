#!/usr/bin/env python

import os

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
    def row(self):
        return self._row

    @property
    def tile(self):
        return self._tile

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
            self._value, self.options = value, [value]
        elif value is None:
            self._value = None 
            self.options = self.allOptions
        else:
            raise ValueError("Invalid value")

    @col.setter
    def col(self, col):
        self._col = col

    @row.setter
    def row(self, row):
        self._row = row

    @tile.setter
    def tile(self, tile):
        self._tile = tile

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return self.__str__()

class CellGroup(object):
    def __init__(self, maxCells=DEF_TILE_BASE ** 2, tileBase=DEF_TILE_BASE):
        self._maxCells = maxCells
        self._tileBase = tileBase
        self._cells = []

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
            print(repr(self._cells))
            raise ValueError("Too many cells")
        self._cells.append(cell)

class Col(CellGroup):
    def __str__(self):
        out = "\n".join(map(lambda c: str(c), self.cells))
        return out

    def __repr__(self):
        return self.__str__()

class Row(CellGroup):
    def __str__(self):
        out = " ".join(map(lambda c: str(c), self.cells))
        return out

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
    def __init__(self, tileBase=DEF_TILE_BASE):
        self._tileBase = tileBase
        self._cells = CellGroup(self._tileBase ** 4)
        self._cols = []
        self._rows = []
        self._tiles = []
        self.initCells()
        self.initCellGroups()

    def initCells(self):
        for n in xrange(self._tileBase ** 4):
            c = Cell(None)
            c.row, c.col = divmod(n, self._tileBase ** 2)
            c.tile = (
                self._tileBase * (n // self._tileBase ** self._tileBase) +
                (n % self._tileBase ** 2) // self._tileBase
            )
            self._cells.addCell(c)

    def initCellGroups(self):
        for n in xrange(self._tileBase ** 2):
            col = Col()
            row = Row()
            tile = Tile()
            for cell in self._cells.cells:
                if cell.col == n:
                    col.addCell(cell)
                if cell.row == n:
                    row.addCell(cell)
                if cell.tile == n:
                    tile.addCell(cell)
            self._cols.append(col)
            self._rows.append(row)
            self._tiles.append(tile)

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
        return(out)

    def __repr__(self):
        return self.__str__()

class Game(object):
    def __init__(self, tileBase=DEF_TILE_BASE):
        self._board = Board()

if __name__ == '__main__':
    os.system('clear')
    b = Board()
    print(str(b))
    print
    print(str(b.cols[0]))
    print
    print(str(b.rows[0]))
    print
    print(str(b.cells.cells[0]))

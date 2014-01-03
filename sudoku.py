#!/usr/bin/env python

import os
import sys

from math import log10

DEF_TILE_BASE = 3

class Cell(object):
    def __init__(self, value=None, tileBase=DEF_TILE_BASE, options=[]):
        self._tileBase = tileBase
        self._col = None
        self._row = None
        self._tile = None
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
        if self._value is None or self._value == 0:
            return " "
        else:
            return self._value

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

    def __str__(self):
        return (
            "[{0:" + str(int(1+log10(self.maxValue))) + "}]"
        ).format(self.value)

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

    def update(self):
# HIERO -> Dit moet worden geimplementeerd
        print("CellGroup() updated")

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
    def __init__(self, values=None, tileBase=DEF_TILE_BASE):
        self._tileBase = tileBase
        self._cellGroup = CellGroup(self._tileBase ** 4)
        self._cols = []
        self._rows = []
        self._tiles = []
        self._initCells(values)
        self._initCellGroups()

    def _initCells(self, values=None):
        for n in xrange(self._tileBase ** 4):
            c = Cell(None, self._tileBase)
            if not values is None and len(values) > 0:
                value, values = values[0:1:], values[1::]
                c.value = int(value)
            self.cellGroup.addCell(c)

    def _initCellGroups(self):
        for n in xrange(self._tileBase ** 2):
            col = Col(self._tileBase ** 2, self._tileBase)
            row = Row(self._tileBase ** 2, self._tileBase)
            tile = Tile(self._tileBase ** 2, self._tileBase)
            for m in self._getColCellNumbers(n):
                col.addCell(self.cellGroup.cells[m])
            for m in self._getRowCellNumbers(n):
                row.addCell(self.cellGroup.cells[m])
            for m in self._getTileCellNumbers(n):
                tile.addCell(self.cellGroup.cells[m])
            self.cols.append(col)
            self.rows.append(row)
            self.tiles.append(tile)

    def getCellCol(self, cell):
        return self.cols[self._getCellColNumber(cell)]

    def _getCellColNumber(self, cell):
        return cell % self._tileBase ** 2

    def getCellRow(self, cell):
        return self.rows[self._getCellRowNumber(cell)]

    def _getCellRowNumber(self, cell):
        return cell // self._tileBase ** 2

    def getCellTile(self, cell):
        return self.tiles[self._getCellTileNumber(cell)]

    def _getCellTileNumber(self, cell):
        return (
            self._tileBase * (cell // self._tileBase ** 3) +
            (cell % self._tileBase ** 2) // self._tileBase
        )

    def _getColCellNumbers(self, col):
        return filter(
            lambda c: self._getCellColNumber(c) == col,
            xrange(self._tileBase ** 4)
        )

    def _getRowCellNumbers(self, row):
        return filter(
            lambda c: self._getCellRowNumber(c) == row,
            xrange(self._tileBase ** 4)
        )

    def _getTileCellNumbers(self, tile):
        return filter(
            lambda c: self._getCellTileNumber(c) == tile,
            xrange(self._tileBase ** 4)
        )

    def setCellValue(self, cell, value):
        self.cells[cell].value = value
# HIERO: Hier moeten de CellGroups geupdatet worden
        self.cols[self._getCellColNumber(cell)].update()
        self.rows[self._getCellRowNumber(cell)].update()
        self.tiles[self._getCellTileNumber(cell)].update()

    @property
    def cell(self, cell):
        if cell >= len(self._cells):
            raise ValueError("Invalid cell")
        return self.cellGroup[cell]

    @property
    def cellGroup(self):
        return self._cellGroup

    @property
    def cells(self):
        return self.cellGroup.cells

    def col(self, col):
        if col >= self._tileBase ** 2:
            raise ValueError("Invalid col")
        return self.cols[col]

    @property
    def cols(self):
        return self._cols

    def row(self, row):
        if row >= self._tileBase ** 2:
            raise ValueError("Invalid row")
        return self.rows[row]

    @property
    def rows(self):
        return self._rows

    def tile(self, tile):
        if tile >= self._tileBase ** 2:
            raise ValueError("Invalid tile")
        return self.tiles[tile]

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
        "029001700" +
        "800000306" +
        "007000004" + 
        "100005000" + 
        "600023009" +
        "900008000" + 
        "004000003" +
        "500000402" +
        "013002500",

        "100002760" + 
        "200001008" + 
        "036007004" + 
        "000060872" + 
        "607029000" + 
        "000000000" + 
        "080070300" + 
        "013000500" + 
        "000010097",

        "000040700" + 
        "000001050" + 
        "840002003" + 
        "100500030" +
        "609007000" +
        "500100020" +
        "780005001" +
        "000006040" +
        "000030200"
    ]
    os.system('clear')
    b = Board(boards[1])
    print(b)
    print
    print(b.getCellCol(9))
    print
    print(b.getCellTile(27))
    print
    print(b.getCellRow(1))
    print
# Dit moet vervangen worden door een Board()-method
    b.setCellValue(1,2)
    print
    print(b.getCellRow(1))
    sys.exit(0)

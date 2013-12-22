#!/usr/bin/env python

import os

DEF_GRID_BASE = 3

class Cell(object):
    def __init__(self, value=None, gridBase=DEF_GRID_BASE, options=[]):
        self.__gridBase = gridBase
        self.maxValue = self.__gridBase ** 2
        self.allOptions = range(1, self.maxValue + 1)
        self.options = self.allOptions
        self.value = value

    @property
    def maxValue(self):
        return self.__maxValue

    @property
    def options(self):
        return tuple(self.__options)

    @property
    def value(self):
        return self.__value

    @maxValue.setter
    def maxValue(self, maxValue):
        self.__maxValue = maxValue

    @options.setter
    def options(self, options=[]):
        self.__options = set(options)

    def delOptions(self, options=[]):
       self.options = tuple(set(self.options) - set(options))

    @value.setter
    def value(self, value=None):
        if value in self.options:
            self.__value, self.options = value, [value]
        elif value is None:
            self.__value = None 
            self.options = self.allOptions
        else:
            raise ValueError("Invalid value")

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return self.__str__()

class CellList(object):
    def __init__(self, values=[], gridBase=DEF_GRID_BASE):
        self.__gridBase = gridBase
        self.__maxCells = self.__gridBase ** 2
        self.cells = values

    @property
    def cells(self):
        return self.__cells

    @cells.setter
    def cells(self, values=None):
        if values is None or len(values) == 0:
            values = range(1, self.__maxCells + 1)

        if len(set(values)) != self.__maxCells and set(values) != set([None]):
            raise ValueError("Non-unique or invalid number of values")

        self.__cells = [Cell(v) for v in values]

class Tile(CellList):
    def __str__(self):
        out = ""
        for y in xrange(self.__gridBase):
            s = y * self.__gridBase
            e = s + self.__gridBase
            out += "{0}\n".format(
                    " ".join(map(lambda c: str(c), self.cells[s:e]))
            )
        return out

    def __repr__(self):
        return self.__str__()

class Row(CellList):
    pass

class Row(CellList):
    pass

class Board(object):
    def __init__(self, gridBase=DEF_GRID_BASE):
        self.__gridBase = gridBase
        self.__maxTiles = self.__gridBase ** 2
        self.__tiles = [Tile() for n in xrange(self.__maxTiles)]

    @property
    def tiles(self):
        return self.__tiles

    @property
    def col(self, col):
        pass

    @property
    def row(self, row):
        pass

    @col.setter
    def col(self, col):
        pass

    @row.setter
    def row(self, row):
        pass

class Game(object):
    def __init__(self, gridBase=DEF_GRID_BASE):
        self.__board = Board()

if __name__ == '__main__':
    os.system('clear')
    b = Board()
    print repr(b.tiles[0])


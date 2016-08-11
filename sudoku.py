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

    def __init__(self):
        pass

def main():
    print(Cell())
    print(Column())
    print(Row())
    print(Tile())
    t = Tile()
    print(t.NEWLINE_POSITION)

if __name__ == '__main__':
    main()

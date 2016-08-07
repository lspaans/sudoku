#!/usr/bin/env python

class Cell(object):

    VALUE = 0

    def __init__(self, value=VALUE):
        self.value = value

    @property
    def value(self):
        return(self._value)

    @value.setter
    def value(self, value):
        if (
            isinstance(value, (int,)) and
            0 <= value < 10
        ):
            self._value = value
        else:
            raise ValueError(
                "Illegal Cell-value: '{value}'".format(value=value)
            )

    def __str__(self):
        return("({value})".format(value=self.value))


class CellGroup(object):

    def __init__(self, cells=[]):
        self._init_cells(cells)

    def _init_cells(self, cells=[]):
        self.cells = []

    def add_cell(self, cell):
        if isinstance(cell, Cell):
            self._cells.append(cell)
        else:
            raise ValueError(
                "Illegal object-type: '{type}'".format(type=type(cell))
            )

    @property
    def cells(self):
        return(self._cells)

    @cells.setter
    def cells(self, cells):
        for cell in cells:
            self.add_cell(cell)


def main():
    c = Cell(9)
    print(c)

if __name__ == '__main__':
    main()

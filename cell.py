#!/usr/bin/env python

class Cell(object):

    VALUE = 0

    def __init__(self, value=None):
        if value is None:
            value = self.VALUE

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
        return("[{value}]".format(value=self.value))


    def __repr__(self):
        return(self.__str__())


class CellGroup(object):

    MAXIMUM = 1
    NEWLINE_POSITION = MAXIMUM
    SEPARATOR = " "
    UNIQUE = False

    def __init__(self, cells=None, unique=None, maximum=None):

        self.unique = self.UNIQUE if unique is None else unique
        self.maximum = self.MAXIMUM if maximum is None else maximum

        if cells is None:
            if self.unique:
                cells = map(lambda n: Cell(n), xrange(1, self.maximum+1))
            else:
                cells = map(lambda n: Cell(), xrange(self.maximum))

        self._init_cells(cells)


    def _init_cells(self, cells=[]):
        self._cells = []
        self.cells = cells


    def add(self, cell):
        if isinstance(cell, Cell):
            if (
                self.unique and
                cell.value in map(lambda c: c.value, self.cells)
            ):
                raise ValueError(
                    "Non-unique Cell-value: '{value}'".format(value=cell.value)
                )
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
            self.add(cell)


    @property
    def maximum(self):
        return(self._maximum)


    @maximum.setter
    def maximum(self, maximum):
        if isinstance(maximum, (int, long)):
            self._maximum = maximum
        else:
            raise ValueError(
                "Illegal value for 'maximum': '{value}'".format(value=maximum)
            )


    @property
    def unique(self):
        return(self._unique)


    @unique.setter
    def unique(self, unique):
        if isinstance(unique, bool):
            self._unique = unique
        else:
            raise ValueError(
                "Illegal value for 'unique': '{value}'".format(value=unique)
            )


    def __str__(self):
        return(
            "".join(map(lambda (n, value): "{value}{separator}".format(
                value=value,
                separator=(
                    "\n" if n % self.NEWLINE_POSITION == 0 else self.SEPARATOR
                )
            ),
            enumerate(self.cells, start=1)
        )).rstrip())


    def __repr__(self):
        return(self.__str__())

#!/usr/bin/env python3

"""A Sudoku puzzle solver"""

import sys

# From in air entertainment set in Boeing Dreamliner (KLM flight)
EASY = (
    ".5.1968.." +
    ".8.342956" +
    ".36857142" +
    ".6372.514" +
    "427615389" +
    "195.8326." +
    "51297463." +
    "378261.9." +
    "..9538.2."
)

# From iOS Sudoku app
INSANE = (
    "..5.6.98." +
    "7.9.2.6.1" +
    "42....7.." +
    "..3.1...." +
    "..74..3.8" +
    "1........" +
    "....7...." +
    "6..1..89." +
    ".....3.2."
)

# https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html
HARDEST = (
    "8........" +
    "..36....." +
    ".7..9.2.." +
    ".5...7..." +
    "....457.." +
    "...1...3." +
    "..1....68" +
    "..85...1." +
    ".9....4.."
)

class Unsolvable(Exception):
    """Raised when Sudoku cannot be solved"""


class Cell(object):
    """Represents a Sudoku cell."""

    def __init__(self, value):
        self._value = None
        self.value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        if not isinstance(value, int) or not 0 <= value <= 9:
            raise ValueError("invalid value: \"{}\"".format(value))

        self._value = value

    def show(self):
        sys.stdout.write(str(self))

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value)

    def __str__(self):
        return " {} ".format(self.value if self.value != 0 else '.')

    value = property(get_value, set_value)


class CellList(object):
    """Represents Sudoku columns, grids, rows and board cells."""

    _FORCE_UNIQUE = True
    _GROUP_BY = 9
    _NUMBER_OF_CELLS = 9

    def __init__(self, cells):
        self._cells = None
        self.cells = cells

    def __getitem__(self, idx):
        return self.cells[idx]

    def __setitem__(self, idx, cell):
        self.cells[idx].value = cell.value

    @classmethod
    def from_text(cls, text):
        return cls([Cell(int(c) if c.isdigit() else 0) for c in text])

    def get_cells(self):
        return self._cells

    def set_cells(self, cells):
        self._cells = []

        if not isinstance(cells, (list, tuple)):
            raise TypeError(
                "invalid argument type: \"{}\"".format(type(cells).__name__)
            )
        if len(cells) != self._NUMBER_OF_CELLS:
            raise ValueError("wrong number of cells")
        for n, cell in enumerate(cells):
            if not isinstance(cell, Cell):
                raise TypeError(
                    "invalid argument type in cell list: \"{}\"".format(
                        type(cell).__name__
                    )
                )
            if (
                cell.value == 0 or
                not self._FORCE_UNIQUE or (
                    self._FORCE_UNIQUE and
                    cell not in self
                )
            ):
                self._cells.append(cell)
            else:
                raise ValueError(
                    "duplicate cell value: \"{}\"".format(cell.value)
                )

    def get_empty_cell_indices(self):
        return [n for n, cell in enumerate(self.cells) if cell.value == 0]

    def get_missing_numbers(self):
        return list(
            set(range(1, 10)) - set([cell.value for cell in self.cells])
        )

    def show(self):
        sys.stdout.write(str(self))

    def __contains__(self, cell):
        if not isinstance(cell, Cell):
            raise TypeError(
                "invalid argument type: \"{}\"".format(cell.__class__.__name__)
            )

        return cell.value in [c.value for c in self.cells]

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.cells))

    def __str__(self):
        return "".join(
            (
                str(cell) + ("" if n % self._GROUP_BY else "\n")
            ) for n, cell in enumerate(self.cells, start=1)
        )

    cells = property(get_cells, set_cells)
    empty_cell_indices = property(get_empty_cell_indices)
    missing_numbers = property(get_missing_numbers)


class Column(CellList):
    """Implementation of CellList for simulating Sudoku rows."""

    _GROUP_BY = 1


class Grid(CellList):
    """Implementation of CellList for simulating Sudoku grids."""

    _GROUP_BY = 3


class Row(CellList):
    """Implementation of CellList for simulating Sudoku rows."""

    _GROUP_BY = 9


class BoardCellList(CellList):
    """Implementation of CellList for simulating all Sudoku cells."""

    _FORCE_UNIQUE = False
    _GROUP_BY = 81
    _NUMBER_OF_CELLS = 81

    def get_missing_numbers(self):
        return


class Board(object):
    """Represents a Sudoku board."""

    def __init__(self, celllists):
        self._cells = None
        self._celllists = None
        self._columns = None
        self._grids = None
        self._rows = None
        self.celllists = celllists

    def __iter__(self):
        for celllist in self.celllists:
            yield celllist

    def __getitem__(self, idx):
        return self.celllist[idx]

    def _init_cells(self):
        self._cells = BoardCellList(
            [cell for celllist in self.celllists for cell in celllist]
        )

    def _init_columns(self):
        self._columns = [
            Column(
                [self.celllists[row][column] for row in range(9)]
            ) for column in range(9)
        ]

    def _init_grids(self):
        self._grids = [
            Grid(
                [self.celllists[3*(n//3)+m//3][(3*n)%9+m%3] for m in range(9)]
            ) for n in range(9)
        ]

    def _init_rows(self):
        self._rows = [
            Row(
                [self.celllists[column][row] for row in range(9)]
            ) for column in range(9)
        ]

    @classmethod
    def from_text(cls, text):
        return cls([CellList.from_text(text[9*n:9+9*n]) for n in range(9)])

    def get_celllists_at_cell_index(self, idx):
        if not 0 <= idx <= 81:
            raise ValueError("invalid cell index: \"{}\"".format(idx))

        return [
            self.columns[idx%9],
            self.grids[(idx//27)*3+(idx%9)//3],
            self.rows[idx//9]
        ]

    def get_column_at_cell_index(self, idx):
        return self.get_celllists_at_cell_index(idx)[0]

    def get_grid_at_cell_index(self, idx):
        return self.get_celllists_at_cell_index(idx)[1]

    def get_row_at_cell_index(self, idx):
        return self.get_celllists_at_cell_index(idx)[2]

    def get_cells(self):
        return self._cells

    def get_celllists(self):
        return self._celllists

    def get_columns(self):
        return self._columns

    def get_grids(self):
        return self._grids

    def get_rows(self):
        return self._rows

    def set_celllists(self, celllists):
        self._celllists = []

        if not isinstance(celllists, (list, tuple)):
            raise TypeError(
                "invalid argument type: \"{}\"".format(type(celllists).__name__)
            )
        if len(celllists) != 9:
            raise ValueError("wrong number of cell sets")
        for celllist in celllists:
            if not isinstance(celllist, CellList):
                raise TypeError(
                    "invalid argument type in cell set list: \"{}\"".format(
                        type(celllist).__name__
                    )
                )

            self._celllists.append(celllist)

        self._init_cells()
        self._init_columns()
        self._init_grids()
        self._init_rows()

    def show(self):
        sys.stdout.write(str(self))

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.celllists))


    def __str__(self):
        return "".join([str(celllist) for celllist in self.celllists])

    cells = property(get_cells)
    celllists = property(get_celllists, set_celllists)
    columns = property(get_columns)
    grids = property(get_grids)
    rows = property(get_rows)


class Sudoku(object):
    """Represents a Sudoku puzzle."""

    def __init__(self, board=None):
        self._board = None
        self.board = board or self.get_generated_board()

    def get_board(self):
        return self._board

    def set_board(self, board):
        if not isinstance(board, Board):
            raise TypeError("invalid argument type: \"{}\"".format(
                    board.__class__.__name__
            ))

        self._board = board

    def show(self):
        sys.stdout.write(str(self))

    def solve(self):
        board_then = []
        board_now = [cell.value for cell in self.board.cells]

        while self.board.cells.empty_cell_indices and board_then != board_now:
            self.solve_cell_index_based()
            self.solve_number_based()

            board_then = board_now
            board_now = [cell.value for cell in self.board.cells]

        if self.board.cells.empty_cell_indices:
            raise Unsolvable("**meh**")

    def solve_cell_index_based(self):
        for idx in self.board.cells.empty_cell_indices:
            celllists = self.board.get_celllists_at_cell_index(idx)
            missing_numbers = set(celllists[0].missing_numbers)

            for celllist in celllists[1:]:
                missing_numbers &= set(celllist.missing_numbers)

            if len(missing_numbers) == 1:
                self.board.cells[idx] = Cell(missing_numbers.pop())

    def solve_number_based(self):
        for idx in self.board.cells.empty_cell_indices:
            celllists = self.board.get_celllists_at_cell_index(idx)
            missing_numbers = set(celllists[0].missing_numbers)

            # HIERO


    @staticmethod
    def get_generated_board():
        """
        To be implemented
        """
        return Board.from_text(EASY)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, repr(self.board))

    def __str__(self):
        return "\n{}\n".format("╋".join([
            "━" * 3 * len(str(self.board.cells[0])) for _ in range(3)
        ])).join([
            "\n".join([
                "┃".join([
                    "".join([
                        str(cell) for cell in row[3*m:3+3*m]
                    ]) for m in range(3)
                ]) for row in self.board.rows[3*n:3+3*n]
            ]) for n in range(3)
        ])

    board = property(get_board, set_board)


def main():
    """The Sudoku solver's main function — started automatically when the
    script is executed directly."""

    #sudoku = Sudoku(Board.from_text(EASY))
    #sudoku = Sudoku(Board.from_text(INSANE))
    sudoku = Sudoku(Board.from_text(HARDEST))
    try:
        sudoku.solve()
    except Unsolvable as exc:
        print("Unsolvable: \"{}\"! final state:\n{}\n".format(exc, sudoku))
        return 1
    except KeyboardInterrupt as exc:
        print("Interrupted! final state:\n{}\n".format(sudoku))
        return 1

    print("Solution:\n{}\n".format(sudoku))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python

import sudoku

def main():
    board = sudoku.Board(
        "...82...3" +
        "..49.5..." +
        "2.9......" +
        "8..7..6.5" +
        "14.....39" +
        "9.7..4..2" +
        "......5.1" +
        "...5.63.." +
        "3...82..."
    )
    print(board)
    print
    print(board.rows[0])
    print
    print(board.columns[0])
    print
    print(board.tiles[0])
    print
    for position, cell in enumerate(board.cells):
        print((
            "Cell: " +
            "position={position}," +
            "value={value}," +
            "column={column}," +
            "row={row}," +
            "tile={tile},"
        ).format(
            position=position,
            value=cell.value,
            column=board.get_column(position),
            row=board.get_row(position),
            tile=board.get_tile(position)
        ))

if __name__ == '__main__':
    main()

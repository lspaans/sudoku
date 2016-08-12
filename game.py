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

if __name__ == '__main__':
    main()

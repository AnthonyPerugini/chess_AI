#! /home/anthony/miniconda3/envs/chess/bin/python
from Board import Board

DEPTH = 4
MAXVAL = float('inf')
MINVAL = float('-inf')

board = Board()


while board.outcome() is None:
    value, best_moves = Board.minimax(board, DEPTH, MINVAL, MAXVAL)
    best_move = best_moves[-1]
    board.push(best_move)
    print(board)
    print(f'{board.value()=}')
    print(board.minimax_counter)
    board.reset_counter()
    print()



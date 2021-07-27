#! /home/anthony/miniconda3/envs/chess/bin/python
from Board import Board

DEPTH = 2
MAXVAL = float('inf')
MINVAL = float('-inf')

board = Board('r6k/ppp2ppp/1qn5/8/2Q5/2P5/P1P3PP/R1K4R b - - 30 35')

while board.outcome() is None:
    value, best_moves = Board.minimax(board, DEPTH, MINVAL, MAXVAL)
    try:
        best_move = best_moves[-1]
    except:
        for move in board.legal_moves:
            board.push(move)
            print(move, board.value())
            board.pop()
    board.push(best_move)
    print(board)
    print(f'{board.value()=}')
    print(f'{board.new_board_states=}')
    print(f'{board.total_board_states=}')
    print(f'{len(board.memo)=}')
    print()



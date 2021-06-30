import chess
import numpy as np


class Board(chess.Board):

    values = {'K': 900, 'Q': 90, 'R': 50, 'B': 30, 'N': 30, 'P': 10, \
              'k': -900, 'q': -90, 'r': -50, 'b': -30, 'n': -30, 'p': -10}

    def value(self):
        val = 0
        piece_positions = self.fen().split(' ')[0]
        for piece in piece_positions:
            if piece not in Board.values.keys():
                continue
            val += Board.values[piece] 
        return val

    @classmethod
    def minimax(cls, board, depth): # returns a (value, best_move) tuple

        if depth == 0 or board.outcome():
            return board.value(), None

        if board.turn:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                value, best_move = max((value, best_move), Board.minimax(board, depth - 1), key=lambda x: x[0])
                board.pop()
            return value, move

        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                value, best_move = min((value, best_move), Board.minimax(board, depth - 1), key=lambda x: x[0])
                board.pop()
            return value, move
                

if __name__ == '__main__':
    MAX_DEPTH = 5
    board = Board('rnbqkbnr/pp1ppppp/8/2p5/3P4/5N2/PPP1PPPP/RNBQKB1R w KQkq - 1 2')
    for move in board.legal_moves:
        print(move)
    value, best_move = Board.minimax(board, 1)
    print(f'whites best move: {best_move}, {value=}')
        

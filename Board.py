import chess
import numpy as np


class Board(chess.Board):

    values = {'K': 900, 'Q': 90, 'R': 50, 'B': 30, 'N': 30, 'P': 10, \
              'k': -900, 'q': -90, 'r': -50, 'b': -30, 'n': -30, 'p': -10}

    MOBILTY_WEIGHT = 1

    def value(self, mobility_weight=1, center_control_weight=1):
        val = 0
        piece_positions = self.fen().split(' ')[0]
        for piece in piece_positions:
            if piece not in Board.values.keys():
                continue
            val += Board.values[piece] 

        # piece mobility
        val += self.legal_moves.count() * mobility_weight

        # king safety
        
        
        # center control
        for square in (chess.D4, chess.D5, chess.E4, chess.E5):
            attackers = self.attackers(self.turn, square)
            num_attackers = len(attackers)
            val += num_attackers * center_control_weight

        # pawn structure

    
    @classmethod
    def minimax(cls, board, depth, last_move=None): # returns a (value, best_move) tuple

        if depth == 0 or board.outcome():
            return board.value(), []

        if board.turn:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                cur_val, cur_path = Board.minimax(board, depth - 1, move)
                if value < cur_val:
                    value = cur_val
                    best_path = cur_path
                board.pop()

            best_path.append(last_move)

            return value, best_path

        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                cur_val, cur_path = Board.minimax(board, depth - 1, move)
                if value > cur_val:
                    value = cur_val
                    best_path = cur_path
                board.pop()

            best_path.append(last_move)

            return value, best_path
                

if __name__ == '__main__':
    MAX_DEPTH = 5
    board = Board('rnbqkbnr/pp1ppppp/8/2p5/3P4/5N2/PPP1PPPP/RNBQKB1R w KQkq - 1 2')
    value, best_path = Board.minimax(board, 3)
    print(f'whites best move: {best_path}, {value=}')
        

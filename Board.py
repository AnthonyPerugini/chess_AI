import chess
import numpy as np
from collections import defaultdict
from Piece_Square_Tables import Piece_Tables

class Board(chess.Board):

    minimax_counter = 0
    minimax_counter_2 = 0
    plus_minus = {True: 1, False: -1}
    memo = defaultdict(int)
    values = {'K': 900, 'Q': 90, 'R': 50, 'B': 30, 'N': 30, 'P': 10, \
              'k': -900, 'q': -90, 'r': -50, 'b': -30, 'n': -30, 'p': -10}

    @classmethod
    def reset_counter(cls):
        cls.minimax_counter = 0

    @classmethod
    def reset_counter2(cls):
        cls.minimax_counter_2 = 0

    @classmethod
    def reset_memo(cls):
        cls.memo = defaultdict(int)

    def serialize(self):
        return self.fen().split(' ')[0]


    def value(self, mobility_weight=1, center_control_weight=1):

        if self.outcome():
            d = {'1-0': float('inf'), '0-1': float('-inf'), '1/2-1/2': 0}
            return d[self.outcome().result()]

        if not Board.memo[self.serialize()]:
            Board.minimax_counter += 1

            val = 0
            for pos, piece in self.piece_map().items():
                piece = piece.symbol()

                pos = -pos + 63
                row, col = divmod(pos, 8)
                col = -col + 7

                val += Board.values[piece]
                val += Piece_Tables[piece][row][col] * Board.plus_minus[self.turn]
                
            # piece mobility for both players
            piece_mobility = self.legal_moves.count() * mobility_weight 
            val += piece_mobility * Board.plus_minus[self.turn]
            self.turn = not self.turn
            piece_mobility = self.legal_moves.count() * mobility_weight 
            val += piece_mobility * Board.plus_minus[self.turn]
            self.turn = not self.turn
            
            # king safety
            
            
            # center control
            for square in (chess.D4, chess.D5, chess.E4, chess.E5):
                attackers = self.attackers(self.turn, square)
                num_attackers = len(attackers)
                center_control = num_attackers * center_control_weight

            val += center_control * Board.plus_minus[self.turn]

            self.turn = not self.turn

            for square in (chess.D4, chess.D5, chess.E4, chess.E5):
                attackers = self.attackers(self.turn, square)
                num_attackers = len(attackers)
                center_control = num_attackers * center_control_weight 

            val += center_control * Board.plus_minus[self.turn]

            self.turn = not self.turn

            # pawn structure TODO

            Board.memo[self.serialize()] = val

        else:
            Board.minimax_counter_2 += 1

        return Board.memo[self.serialize()]



    
    @classmethod
    def minimax(cls, board, depth, a, b, last_move=None):

        if depth == 0 or board.outcome():
            return board.value(), []

        if board.turn:
            value = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                cur_val, cur_path = Board.minimax(board, depth - 1, a, b, move)
                if cur_val > value:
                    value = cur_val
                    best_path = cur_path
                board.pop()

                if value >= b:
                    break
                a = max(a, value)

        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                cur_val, cur_path = Board.minimax(board, depth - 1, a, b, move)
                if cur_val < value:
                    value = cur_val
                    best_path = cur_path
                board.pop()

                if value <= a:
                    break
                b = min(b, value)

        if last_move:
            best_path.append(last_move)

        return value, best_path
                

if __name__ == '__main__':
    DEPTH = 4
    MAXVAL = float('inf')
    MINVAL = float('-inf')

    # board = Board('rnbqkbnr/pp1ppppp/8/2p5/3P4/5N2/PPP1PPPP/RNBQKB1R w KQkq - 1 2')
    board = Board()

    for _ in range(20):
        value, best_path = Board.minimax(board, DEPTH, MINVAL, MAXVAL)
        best_move = best_path[-1]
        board.push(best_move)
        print(board)
        print(f'{board.value()=}')
        print(f'{board.minimax_counter=}')
        print(f'{board.minimax_counter_2=}')
        board.reset_counter()
        board.reset_counter2()
        print()

        

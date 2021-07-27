import chess
import numpy as np
from collections import defaultdict
from Piece_Square_Tables import piece_tables, piece_values

class Board(chess.Board):

    new_board_states = 0
    total_board_states = 0
    plus_minus = {True: 1, False: -1}
    memo = defaultdict(int)

    @classmethod
    def reset_counter(cls):
        cls.new_board_state = 0

    @classmethod
    def reset_counter2(cls):
        cls.seen_board_state = 0

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
            Board.new_board_states += 1

            val = 0
            for pos, Piece in self.piece_map().items():

                piece = Piece.symbol()
                color = Piece.color

                pos = -pos + 63
                row, col = divmod(pos, 8)
                col = -col + 7

                val += piece_values[piece]
                piece_position_value = piece_tables[piece][row][col] * Board.plus_minus[color]
                val += piece_position_value

                
            # piece mobility for both players
            piece_mobility = self.legal_moves.count() * mobility_weight 
            val += piece_mobility * Board.plus_minus[self.turn]
            self.turn = not self.turn
            piece_mobility = self.legal_moves.count() * mobility_weight 
            val += piece_mobility * Board.plus_minus[self.turn]
            self.turn = not self.turn
            
            # king safety
            
            
            # center control
            # for square in (chess.D4, chess.D5, chess.E4, chess.E5):
            #     attackers = self.attackers(self.turn, square)
            #     opposing_attackers = self.attackers(not self.turn, square)
            #     num_attackers = len(attackers) - len(opposing_attackers)

            #     center_control = num_attackers * center_control_weight
            #     val += center_control * Board.plus_minus[self.turn]


            # pawn structure TODO

            Board.memo[self.serialize()] = val

        Board.total_board_states += 1

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

                a = max(a, value)
                if a >= b:
                    break

        else:
            value = float('inf')
            for move in board.legal_moves:
                board.push(move)
                cur_val, cur_path = Board.minimax(board, depth - 1, a, b, move)
                if cur_val < value:
                    value = cur_val
                    best_path = cur_path
                board.pop()

                b = min(b, value)
                if b <= a:
                    break

        if last_move:
            best_path.append(last_move)

        return value, best_path
                

if __name__ == '__main__':
    board = Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
    print(board.value())
    print(board)
        

import chess
from collections import defaultdict
from Piece_Square_Tables import piece_tables, piece_values

class Board(chess.Board):

    MAXVAL = float('inf')
    MINVAL = float('-inf')
    DEPTH = 4

    new_board_states = 0
    total_board_states = 0

    memo = defaultdict(int)
    plus_minus = {True: 1, False: -1}
    outcome_dict = {'1-0': float('inf'), '0-1': float('-inf'), '1/2-1/2': 0}

    @classmethod
    def reset_new_board_states(cls):
        cls.new_board_states = 0

    @classmethod
    def reset_total_board_states(cls):
        cls.total_board_states = 0

    @classmethod
    def reset_memo(cls):
        cls.memo = defaultdict(int)

    def serialize(self):
        return self.fen().split(' ')[0]

    def show_legal_moves(self):
        moves = [move for move in self.legal_moves]
        for move in moves:
            print(move)

    def generate_move_from_uci(self):
        uci = input("Enter a move or 'help': ")

        if uci.lower() == 'help':
            self.show_legal_moves()
        if uci.lower() == 'im a filthy cheater':
            try:
                self.pop()
                self.pop()
            except IndexError:
                pass
            print(self)
            return False

        try:
            move = chess.Move.from_uci(uci)
        except ValueError:
            return False

        if move not in self.legal_moves:
            return False

        return move


    def value(self, mobility_weight=0.5, center_control_weight=2):

        if self.outcome():
            return Board.outcome_dict[self.outcome().result()]

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
    def minimax(cls, board, depth=None, a=None, b=None, last_move=None):
        
        if depth is None:
            depth = cls.DEPTH
        if a is None:
            a = cls.MINVAL
        if b is None:
            b = cls.MAXVAL

        best_path = []

        if depth == 0 or board.outcome() or board.legal_moves.count() == 0:
            value = board.value()

        elif board.turn:
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
    board = Board('r1b1k1nr/ppp2ppp/2p1p3/2q5/4P3/3B1N2/P1PB1PPP/R2QK2R w KQkq - 0 1')
    board.push(move)
    print(board)
        

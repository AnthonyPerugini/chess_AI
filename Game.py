from Board import Board
from random import choice

class Game():
    def __init__(self, self_play=True):
        self.self_play = self_play
        self.choose_side()
        self.new_game()
        print(self.board, '\n')

    def new_game(self, starting_fen=None):
        if starting_fen is None:
            self.board = Board()
        else:
            self.board = Board(starting_fen)

    def choose_side(self):
        side = int(input('Choose 1 to play as white, or 0 to play as black: '))
        if side == 1:
            self.computer_side = False
        elif side == 0:
            self.computer_side = True
        else:
            print('bad monkey')
            self.choose_side()


    def play(self):

        while self.board.outcome() is None:

            # Computer vs Computer
            if self.self_play:
                value, best_moves = Board.minimax(self.board)
                try:
                    move = best_moves[-1]
                except:
                    move = choice(self.board.legal_moves)


            # Human vs Computer
            else:
                if self.computer_side == self.board.turn:
                    value, best_moves = Board.minimax(self.board)
                    try:
                        move = best_moves[-1]
                    except:
                        move = choice(self.board.legal_moves)

                # humans move
                else:
                    move = False
                    while not move:
                        move = self.board.generate_move_from_uci()
                        
            self.board.push(move)
            print(self.board)
            if self.self_play:
                print(f'{self.board.value()=}')
                print(f'{self.board.new_board_states=}')
                print(f'{self.board.total_board_states=}')
                print(f'{len(self.board.memo)=}')
            print()
            

        winner = {'1-0': 'White wins', '0-1': 'Black wins', '1/2-1/2': 'Game ended in a draw'}[self.board.outcome().result()]
        print(f'Game over! {winner}!')
        


            
        

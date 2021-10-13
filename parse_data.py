import chess.pgn
import os
import pickle
from collections import defaultdict
from Board import Board


os.chdir('data/processed')
master_games = defaultdict(tuple)

count = 0
failed_count = 0

for pgn in os.listdir():
    try:
        player_name = pgn.split('.')[0]
        print(f'parsing games from: {player_name}...')
        player_games = open(pgn)
        while game := chess.pgn.read_game(player_games):
            ww, bw = {'1-0': (1, 0), '0-1': (0, 1), '1/2-1/2': (0, 0), '*': (None, None)}[game.headers['Result']]
            if ww is None:
                print(f'\t* result found, skipping game#{count + failed_count}')
                failed_count += 1
                continue

            board = Board()

            for move in game.mainline_moves():
                board.push(move)
                srl = board.serialize()
                if master_games[srl]:
                    white_wins, black_wins, total_games = master_games[srl]
                    master_games[srl] = (white_wins + ww, black_wins + bw, total_games + 1)
                else:
                    master_games[srl] = (ww, bw, 1)
            count += 1
        print(f'\ttotal parsed count: {count}')
        print(f'\ttotal failed count: {failed_count}')
    except Exception as e:
        print(e)
        failed_count += 1

os.chdir('./..')

with open('master_games', 'wb') as f:
    data = pickle.dumps(master_games)
    f.write(data)
    print(f'master_games successfully saved with a size of {len(master_games)}')
# 
# with open('master_games', 'rb') as f:
#     pickled_binaries = f.read()
#     master_games = pickle.loads(pickled_binaries)
#     print(f'master_games successfully loaded with a size of {len(master_games)}')




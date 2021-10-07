#! /home/spicy/miniconda3/bin/python

# /home/anthony/miniconda3/envs/chess/bin/python
from Game import Game

game = Game(self_play=True, troubleshooting=True)
game.new_game(starting_fen='r1bqr1k1/p2p2pp/2pp1n2/8/3P4/2P2Q2/PP1N1PPP/R2K3R w - - 6 14')
game.play()




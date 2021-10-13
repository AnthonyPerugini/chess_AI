Project Idea:
----

What I would like to do is make a chess AI, using the minimax algorithm.  The chess AI will need to:

* represent the current board state in a serialized form to reduce space?  FEN code?

* generate all legal moves from current board state
* sort moves based on potential merit (pawn takes, captures, checks...)
* select best positional move based on minimax and AB pruning
* 2nd ply will be sorted and evaluated by highest scoring 1st ply moves, and so on.


representing a board position in the smallest amount of space:

	68
		array of ints size (8x8):
			1: white pawn,
			-1: black pawn,
			2: white knight, 
			-2: black knight,
			etc.
			
			extras:
				whos turn it is 0,1
				50-move draw rule
				kingside/queenside castling rights
				if an en-passant capture is possible

	
how many outputs from the NN?
	1972 possible moves
	1882 possible moves for each color (-enemy pawn promotions, -enemy castling)
	1 extra output for [-1,1] board evaluation?

	



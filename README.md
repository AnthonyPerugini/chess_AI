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
	1972 possible moves for both colors combined

	1882 possible moves for each color
		+ queen moves: 1456
		+ knight moves: 336
		+ pawn promotions: 176 (88 for each color)
		+ castling: 4 (2 for each color)


	1 extra output for [-1,1] board evaluation?


generate all possible moves and a map (0: a1a2, 1:a1a3, ...)
	all_moves = []
	moves_lookup = dict()
	position = 0

	for square in [a1-h8]:
		for each piece in [queen, knight, pawn_promotions, castling]:
			board = Board() with piece on square
			generate endsquares
			for endsquare in endsquares:
				add (square -> endsquare) to all_moves
				add d[square -> endsquare] = position
				position += 1

		

thoughts for how to sort chess moves:
	- pawn captures piece
	- moves where a pawn attack a piece
	- captures
	- castling
	- moves that centralize pieces
	- queen moves


OTHER TODOs:
	- deal with 3 move repeats

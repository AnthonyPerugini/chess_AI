Project Idea:
----

What I would like to do is make a chess AI, using the minimax algorithm.  The chess AI will need to:

* represent the current board state in a serialized form to reduce space?  FEN code?

* generate all legal moves from current board state
* sort moves based on potential merit (pawn takes, captures, checks...)
* select best positional move based on minimax and AB pruning
* 2nd ply will be sorted and evaluated by highest scoring 1st ply moves, and so on.




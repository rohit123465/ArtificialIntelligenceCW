Connect is the game environment for this project. The rules of Connect are simple. Each player has a set of pieces, and
they take turns placing their pieces into the columns of the board. The first player that arranges
their pieces into an uninterrupted line of a given size, wins. This line can be horizontal, vertical
or diagonal. Note that for this coursework, unlike ‘Connect 4’, we will vary the number of pieces
required to be in a line to create different environments. The board is defined by a given number
of rows and columns, which will also be varied within this project.

Importantly, the board operates with gravity. Players select a column in which to place their piece,
and their piece will fall to the lowest numbered empty row. For example, suppose that a player
places their piece in column 4. If spaces (0, 4) and (1, 4) are already occupied, then the player’s
piece will fall to position (2, 4)

The goal in this project is to implement and evaluate two versions of adversarial search, namely,
the minimax algorithm with and without alpha-beta pruning. Your algorithm will be applied to
the game of Connect introduced above. There are two overall tasks:
• Task 1: Minimax without pruning, and
• Task 2: Minimax with alpha-beta pruning.

Run the code by running the command python3 runGame.py

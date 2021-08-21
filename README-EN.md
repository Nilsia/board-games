# board-games

Repository made to help some developpers on python

## Fundamental rules

1. The international draughts game is played on a draughtboard with 100 equals squares in turns black and white.

2. The players play on the black squares. There are 50 active squares. []

3. The emplacement of the board requires the 2 players to have on their bottom left tile as a black square.

4. The international draughts is played with 20 white pieces and 20 black pieces. The 20 black pieces and the 20 white pieces are placed on the 4 first rows of each player.

picture


## How the pieces move

1. There are 2 types of pieces : the regular pieces (Rpieces) and the queens.

2. It is always the white which begins. The players play one after the other.

3. An Rpiece has to move forward diagonally; from a square to a empty square.

picture * 2

4. When an Rpiece arrives to the last row, this Rpiece becomes a queen.

picture *2

5. A queen can move backwards or forwards in each empty squares diagonally.

6. For a player, touching one of his pieces, he has to move it if it is possible.

## The taking

1.The taking of a piece is mandatory, as backward as forward.

2. When an Rpiece has an opposing piece next to it, diagonally, and if after the opposing piece there is an empty square, it has to jump over it and fill the empty square. The opposing piece is removed from the board. []

picture * 2

3. When a queen has a piece on one of its diagonal spaces, where behind it there is one or few empty cells. The queen has to jump over it and fill one of the empty cells behind the opposing piece. The opposing piece is removed from the board.

picutres * 2

4. When a Rpiece can eat a opposing piece, and after it can eat another piece diagonally. It has to jump over it and fill the empty cell behind it. All the opposing pieces eaten are removed from the board.

pictures * 2

5. It is the same for the queens; The queen does not have to stop their eat moves id they can eat another piece.

picture * 2

6. It is forbidden to jump over one of your own pieces.

7. It is forbidden to jump over the same opposing pieces but possible to pass on an empty cell.

picture *2

## The Result

A player has won when his opponent:

  * gives up the game XXX
  * cannot play when it is his turn XXX
  * does not have pieces anymore
  * When nobody can win


XXX = not done

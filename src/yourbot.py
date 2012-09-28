"""Implement the assignment in this file, but run "connectfour.py" to
test your code (it will import this file and call pick_move
repeatedly)."""

import random

ROWS = 6
COLS = 7

class yourbot(object):
    """Your implementation goes here. You can store state between
    moves by accessing "self"; initialize in __init__ (constructor)
    and finalize in __del__ (destructor). Counting moves is just a
    silly example of keeping state.
    """
    def __init__(self):
        self.moves = 0

    def __del__(self):
        print 'Computer made %d moves' % (self.moves,)

    def pick_move(self, board, player_color):
        """Pick your move here. This function takes in the board
        state, and returns a column index corresponding to a valid
        move that you want to make (make sure the column isn't full!).

        board: A list of lists, each list representing a column of the
        board. The last item in a sub-list (the highest index) is the
        most recently added tile in that column (closest to the top of
        the board). For example, board[0] contains a list of tiles in
        the leftmost column of the board. Say there is one red tile on
        top of 3 Black tiles in that column, then board[0] will be
        ['B', 'B', 'B', 'R']. There is no padding for locations
        without tiles, but there will always be a (possibly empty)
        list for each column.

        player_color: Either 'B' or 'R', depending on whether your bot
        is playing Black or Red.

        return: A column number 0-6 which is not already full."""
        self.moves += 1
        col = random.choice(range(len(board)))
        while len(board[col]) >= ROWS:
            col = random.choice(range(len(board)))
        return col

def make_callback():
    """Instantiates your bot object and returns a callback."""
    bot = yourbot()
    return bot.pick_move

if __name__ == '__main__':
    print 'Run connectfour.py instead!'

"""Implement the assignment in this file, but run "connectfour.py" to
test your code (it will import this file and call pick_move
repeatedly)."""

import random

ROWS = 6
COLS = 7

class yourbot(object):
    RED_WINS = 1
    BLACK_WINS = 1023
    EMPTY_OR_MIXTURE = 0
    SINGLE_BLACK = 1
    SINGLE_RED = -1
    TWO_BLACK = 10
    TWO_RED = -10
    THREE_BLACK = 50
    THREE_RED = -50

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
        
	print self.static_evaluator(board, player_color)	
        return col

    def static_evaluator(self, board, player_color):
	"""Checks the state of each four blocks in a valid move and returns the 	sum of this board state"""
	total_sum = 0	

	total_sum += self.check_vertical(board)
	total_sum += self.check_horizontal(board)
	total_sum += self.check_right_diagonal(board)
	total_sum += self.check_left_diagonal(board)

	print 'Check vertical: ' + repr(self.check_vertical(board))
	print 'Check horizontal: ' + repr(self.check_horizontal(board))
	print 'Check right diagonal: ' + repr(self.check_right_diagonal(board))
	print 'Check left diagonal: ' + repr(self.check_left_diagonal(board))

	return total_sum

    def chip_value(self, chip_set):
	# Check the number of chips in a 4 chip set and return the sum of the score
	number_of_red = 0
	number_of_black = 0
	for x in chip_set:
	    if x is 'R':
		number_of_red += 1
	    elif x is 'B':
		number_of_black += 1
	
	if (number_of_red > 0 and number_of_black > 0) or (number_of_red == 0 and number_of_black == 0):
	    return 0
	elif number_of_red == 1:
	    return -1
        elif number_of_black == 1:
            return 1
        elif number_of_red == 2:
            return -10
        elif number_of_black == 2:
            return 10
        elif number_of_red == 3:
            return -50
        else:
	    return 50

    def check_vertical(self, board):
	#Go through every vertical possibility and calculate the static evaluation
	vertical_sum = 0 # The values of the evaluator function will be returned here
	
	# Loop over each vertical set of 4 and add the appopriate evaluation
	for col in range(COLS):
	    for row in range(ROWS - 3):
		chips = []
#		print 'Length: ' + repr(len(board[col]))
		for chip in range(row, row + 4):
		    if chip < len(board[col]):
		        chips.append(board[col][chip])
                vertical_sum += self.chip_value(chips)
	return vertical_sum

    def check_horizontal(self, board):
	# Go through every horizontal possibility and calculate the static evaluation
	horizontal_sum = 0

	# Go column by column and crawl up the board
	for col in range(COLS - 3):
	    # Want to check each row
	    for row in range(ROWS):
		chips = []
		for chip in range(col, col + 4):
		   if row < len(board[chip]):
		       chips.append(board[chip][row])
                horizontal_sum += self.chip_value(chips)

	return horizontal_sum

    def check_left_diagonal(self, board):
	# Check the leftward-up diagonals
	left_diagonal_sum = 0

	for col in range(COLS - 1, 2, -1):
	    # Climb up each row
		for row in range(ROWS - 2):
		    chips = []
                    for chip in range(4): # Climb by 4
                        if row + chip < len(board[col - chip]):
			    chips.append(board[col-chip][row+chip])
			left_diagonal_sum += self.chip_value(chips)

	return left_diagonal_sum

    def check_right_diagonal(self, board):
	# Check the rightward-up diagonals
	right_diagonal_sum = 0

	for col in range(COLS - 3):
	    # Climb up each row
	    for row in range(ROWS - 2):
                chips = []
	        for chip in range(4): # Need to climb by 4
                    if row + chip < len(board[col + chip]):
		        chips.append(board[col+chip][row+chip])
                right_diagonal_sum += self.chip_value(chips)

	return right_diagonal_sum

def make_callback():
    """Instantiates your bot object and returns a callback."""
    bot = yourbot()
    return bot.pick_move

if __name__ == '__main__':
    print 'Run connectfour.py instead!'

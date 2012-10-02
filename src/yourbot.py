"""Implement the assignment in this file, but run "connectfour.py" to
test your code (it will import this file and call pick_move
repeatedly)."""

import random
import copy
import time

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
    RED_MOVE = -16
    BLACK_MOVE = 16

    # Values for detection in the evaluation function that a win was detected. Needs to be outside any possible bounds that could be generated
    RED_WIN_DETECTED = -10000
    BLACK_WIN_DETECTED = 10000

    STATIC_START = 512

    best_move = None

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
        self.my_color = player_color
	self.best_move = None 
	
	self.moves += 1

	start = time.clock()

	self.number_searched = 0
	self.number_skipped = 0
	
	col = self.minimax_search(board, player_color, False, 5)

	elapsed = (time.clock() - start)

	print 'Took ' + repr(elapsed) + ' seconds. Searched ' + repr(self.number_searched) + ' moves. Skipped ' + repr(self.number_skipped) + ' moves.\n'
	print 'Column: ' + repr(col) + '\n'
	return col

    def static_evaluator(self, board, player_color):
	"""Checks the state of each four blocks in a valid move and returns the	sum of this board state"""
	
	vertical_sum = self.check_vertical(board)
	horizontal_sum = self.check_horizontal(board)
	right_diagonal_sum = self.check_right_diagonal(board)
	left_diagonal_sum = self.check_left_diagonal(board)

	if vertical_sum == self.RED_WIN_DETECTED or horizontal_sum == self.RED_WIN_DETECTED or right_diagonal_sum == self.RED_WIN_DETECTED or left_diagonal_sum == self.RED_WIN_DETECTED:
	    return self.RED_WINS
	elif vertical_sum == self.BLACK_WIN_DETECTED or horizontal_sum == self.BLACK_WIN_DETECTED or right_diagonal_sum == self.BLACK_WIN_DETECTED or left_diagonal_sum == self.BLACK_WIN_DETECTED:
	    return self.BLACK_WINS

	total_sum = self.STATIC_START + vertical_sum + horizontal_sum + right_diagonal_sum + left_diagonal_sum

	if player_color == 'R':
	    total_sum += self.RED_MOVE
	else:
	    total_sum += self.BLACK_MOVE

	if total_sum < 2:
	    total_sum = 2
	elif total_sum > 1022:
	    total_sum = 1022

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
	    return self.EMPTY_OR_MIXTURE
	elif number_of_red == 1:
	    return self.SINGLE_RED
        elif number_of_black == 1:
            return self.SINGLE_BLACK
        elif number_of_red == 2:
            return self.TWO_RED
        elif number_of_black == 2:
            return self.TWO_BLACK
        elif number_of_red == 3:
            return self.THREE_RED
        elif number_of_black == 3:
	    return self.THREE_BLACK
        elif number_of_red == 4:
            return self.RED_WIN_DETECTED
	else:
	    return self.BLACK_WIN_DETECTED

    def check_vertical(self, board):
	#Go through every vertical possibility and calculate the static evaluation
	vertical_sum = 0 # The values of the evaluator function will be returned here
	
	# Loop over each vertical set of 4 and add the appopriate evaluation
	for col in range(COLS):
	    for row in range(ROWS - 3):
		chips = []
		for chip in range(row, row + 4):
		    if chip < len(board[col]):
		        chips.append(board[col][chip])

		chip_val = self.chip_value(chips)

		if chip_val == self.RED_WIN_DETECTED:
		    return self.RED_WIN_DETECTED
		elif chip_val == self.BLACK_WIN_DETECTED:
		    return self.BLACK_WIN_DETECTED
		else:
	            vertical_sum += chip_val

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

               	chip_val = self.chip_value(chips)

		if chip_val == self.RED_WIN_DETECTED:
		    return self.RED_WIN_DETECTED
		elif chip_val == self.BLACK_WIN_DETECTED:
		    return self.BLACK_WIN_DETECTED
		else:
	            horizontal_sum += chip_val

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

	            chip_val = self.chip_value(chips)

		    if chip_val == self.RED_WIN_DETECTED:
		        return self.RED_WIN_DETECTED
		    elif chip_val == self.BLACK_WIN_DETECTED:
		        return self.BLACK_WIN_DETECTED
		    else:
	                left_diagonal_sum += chip_val

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

                chip_val = self.chip_value(chips)

                if chip_val == self.RED_WIN_DETECTED:
	            return self.RED_WIN_DETECTED
	        elif chip_val == self.BLACK_WIN_DETECTED:
	            return self.BLACK_WIN_DETECTED
	        else:
	            right_diagonal_sum += chip_val

	return right_diagonal_sum

    def next_board_states(self, board, player_color):
	# Gets the next possible board states and returns them in a list.
	results = []

	# Check if a column is full if not, pass in the state
	for state in range (COLS):
	    if len(board[state]) < ROWS - 1:
		# Add the chip to the board and then add it to the results
		new_state = copy.deepcopy(board)
		new_state[state].append(player_color)
	    else:
		new_state = [] # Empty list if the column is filled (Going to use for quickly finding out which column the move is in)
		
	    results.append(new_state)
	return results

    def minimax_search(self, board, player_color, with_alpha_beta, depth_limit):

	"""if with_alpha_beta:

	else:"""
	print 'Best score: ' + repr(self.minimax_no_alpha_beta(board, player_color, 0, depth_limit)) + '\n'

	return self.best_move

    def minimax_no_alpha_beta(self, board, current_color, depth, depth_limit):
	
	# Find the "Infinity" value	
	if self.my_color != current_color:
	    if self.my_color == 'R':
		best_score = self.RED_WINS
	    else:
		best_score = self.BLACK_WINS
	else:
	   if self.my_color == 'R':
		best_score = self.BLACK_WINS
	   else:
		best_score = self.RED_WINS

	# At the depth limit evaluate and return
	if depth == depth_limit:
	    sum = self.static_evaluator(board, current_color)
	    return sum

	else: # Need to go deeper
	    # Set the next player's color
	    if current_color == 'B':
	        new_color = 'R'
	    else:
	        new_color = 'B'

	    current_move = 0 # Tracks the move column

	    for move in self.next_board_states(board, current_color):
		# Increment the number searched
		self.number_searched += 1

		if len(move) == 0: # Board was full where we were trying to place a chip
		    self.number_skipped += 1
		    current_move += 1
		    continue

		# Get a board for each next play state and set the next color
	        score = self.minimax_no_alpha_beta(move, new_color, depth + 1, depth_limit)
	
		score_changed = False	
		if new_color == self.my_color: # Max case
		    if self.my_color == 'R':
    		        if score > best_score:
		            best_score = score
			    scored_changed = True
   		    else: # Black
			if score > best_score:
			    best_score = score
			    score_changed = True
		    
                    if depth == 0 and score_changed:
			self.best_move = current_move 	
		else:				# Min case
		    if self.my_color == 'B':
                        if score < best_score:
		            best_score = score
			    score_changed = True
		    else: # Red
			if score < best_score:
			    best_score = score
			    score_changed = True

		    if depth == 0 and score_changed:
		        self.best_move = current_move

		current_move += 1

	    # Need an arbitrary selection in case we get in a drawn/unwinnable state
	    if self.best_move == None:
		for slot in range(COLS):
		    if len(board[slot]) < ROWS:
			self.best_move = slot

	    return best_score

def make_callback():
    """Instantiates your bot object and returns a callback."""
    bot = yourbot()
    return bot.pick_move

if __name__ == '__main__':
    print 'Run connectfour.py instead!'

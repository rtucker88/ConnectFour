"""Bookkeeping for connect-four. Checks for wins/draws, accepts input
from a human, and prints the board. You shouldn't need to modify this
code to complete the assignment; your implementation should go in
yourbot.py."""

import copy
import random
import yourbot

ROWS = yourbot.ROWS
COLS = yourbot.COLS
PLAYER_COLORS = ['B', 'R']
INV_COLORS = {c:i for i, c in enumerate(PLAYER_COLORS)}

def main():
    play(yourbot.make_callback(), human_player_callback)

def check_windraw(board):
    def check_same(points):
        result_set = set()
        for rown, coln in points:
            if (coln < len(board) and coln >= 0
                and len(board[coln]) > rown and rown >= 0):
                result_set.add(board[coln][rown])
            else:
                return None
        if len(result_set) != 1 or None in result_set:
            return None
        else:
            return list(result_set)[0]
    def check_right_diag(rown, coln):
        return check_same(((rown + i, coln + i) for i in range(4)))
    def check_left_diag(rown, coln):
        return check_same(((rown + i, coln - i) for i in range(4)))
    def check_row(rown, coln):
        return check_same(((rown, coln + i) for i in range(4)))
    def check_col(rown, coln):
        return check_same(((rown + i, coln) for i in range(4)))
    for coln in range(len(board)):
        for rown, _ in enumerate(board[coln]):
            point = (rown, coln)
            result = (check_right_diag(rown, coln) or
                      check_left_diag(rown, coln) or
                      check_row(rown, coln) or
                      check_col(rown, coln))
            if result is not None:
                return result
    for coln in range(len(board)):
        if len(board[coln]) < ROWS:
            return None
    return 0

def play(first_player_callback, second_player_callback,
         rows=ROWS, cols=COLS, do_prints=True):
    # The board is one list per column
    board = [[] for i in range(cols)]
    players = [first_player_callback, second_player_callback]
    # Choose which function is B Player randomly
    random.shuffle(players)
    current_player = 0
    while True:
        winner = check_windraw(board)
        if winner is not None:
            break
        column_move = int(players[current_player](
                copy.deepcopy(board), PLAYER_COLORS[current_player]))
        # The player function should always return a valid move:
        assert 0 <= column_move < cols
        assert len(board[column_move]) < rows
        # Apply the move
        board[column_move].append(PLAYER_COLORS[current_player])
        if do_prints:
            print '%s Player adds to column %d' % (
                PLAYER_COLORS[current_player], column_move)
        print_board(board)
        # The next player gets a turn now
        current_player += 1
        current_player %= 2
    if winner == 0:
        if do_prints:
            print 'Draw'
        return (board, None)
    else:
        if do_prints:
            print '%s Player wins!' % (winner,)
        return (board, players[INV_COLORS[winner]])

def print_board(board):
    for rown in range(ROWS):
        print '|',
        for coln in range(len(board)):
            if len(board[coln]) > ROWS - rown - 1:
                print board[coln][ROWS - rown - 1],
            else:
                print '_',
        print '|'
    print '-' * (2 * len(board) + 3)
    print '|%s |' % (''.join(' %s' % (str(d),)
                             for d in range(len(board))),)
    print

def human_player_callback(board, player_color):
    choice = raw_input('It\'s %s Player\'s turn! Pick a column 0-%d: '
                       % (player_color, len(board) - 1))
    while True:
        try:
            choice_int = int(choice)
            if choice_int in range(len(board)):
                if len(board[choice_int]) >= ROWS:
                    choice = raw_input(
                        '%s Player, that column is full! Please pick again: '
                        % (player_color,))
                    continue
                else:
                    return choice_int
        except ValueError, e:
            pass
        choice = raw_input(
            '%s Player, please enter a column number between 0 and %d inclusive: '
            % (player_color, len(board) - 1))

if __name__ == '__main__':
    main()

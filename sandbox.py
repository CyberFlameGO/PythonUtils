# tictactoe
# Description:
# A game of tic-tac-toe.
#


class TicTacToe:
    """
    A game of tic-tac-toe.
    """
    def __init__(self):
        self.board = [None] * 9
        self.winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]

    def draw(self):
        """
        Draw the board.
        """
        print('   |   |')
        print(' ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8])
        print('   |   |')

    def legal_moves(self):
        """
        Return a list of legal moves.
        """
        moves = []
        for i in range(9):
            if self.board[i] is None:
                moves.append(i)
        return moves

    def make_move(self, position, player):
        """
        Make a move on the board.
        """
        self.board[position] = player

    def has_winner(self):
        """
        Return whether or not there is a winner.
        """
        for player in 'XO':
            for combo in self.winning_combos:
                if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == player:
                    return True

        return False

    def game_over(self):
        """
        Return whether or not the game is over.
        """
        return

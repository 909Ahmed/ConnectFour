import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        column = 0
        max_ele = - 2 ** 31
        for col in range(7):
            if not self.isFull(board, col):

                val = self.minimax(self.fill(board, col, 1), -1, max_ele, 2 ** 31, 4)
                if val > max_ele:
                    max_ele = val
                    column = col

        return column
    



    def minimax(self, board, player, alpha, beta, depth):
        
        complete = self.isComplete(board)
        eval = self.evaluation_function(board)

        if depth == 0 or complete or abs(eval) >= 1000000000:
            return eval
        
        if player == 1:

            val = - 2 ** 31
            for col in range(7):
                if not self.isFull(board, col):

                    val = max(self.minimax(self.fill(board, col, player), -player, alpha, beta, depth - 1), val)
                    alpha = max(alpha, val)
                    if alpha >= beta:
                        break

            return alpha

        else:

            val = 2 ** 31
            for col in range(7):
                if not self.isFull(board, col):

                    val = min(self.minimax(self.fill(board, col, player), -player, alpha, beta, depth - 1), val)
                    beta = min(beta, val)
                    if alpha >= beta:
                        break

            return beta
        
    def isFull(self, board, col):
        return (board[0][col] != 0)

    def isComplete(self, board):
        return not np.isin(0, board[0])

    def fill(self, board, col, player):

        new_board = np.copy(board)

        for i in range(5, -1, -1):
            if new_board[i][col] == 0:
                
                if player == 1:
                    new_board[i][col] = 1
                else:
                    new_board[i][col] = 2
                return new_board

        return new_board


    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        
        win_one = "1111"
        win_two = "2222"

        eval = 0

        if self.scores(board, win_one):
            return 1000000000
        elif self.scores(board, win_two):
            return -1000000000
        
        eval += 10000 * (self.scores(board, "1110") + self.scores(board, "0111"))
        eval += 100 * (self.scores(board, "1100") + self.scores(board, "0011"))
        eval += 100 * (self.scores(board, "1001") + self.scores(board, "1001"))
        eval += 100 * (self.scores(board, "1010") + self.scores(board, "1010"))
        eval += 100 * (self.scores(board, "0110") + self.scores(board, "0110"))
        eval += 100 * (self.scores(board, "0101") + self.scores(board, "0101"))

        eval -= 10000 * (self.scores(board, "2220") + self.scores(board, "0222"))
        eval -= 100 * (self.scores(board, "2200") + self.scores(board, "0022"))
        eval -= 100 * (self.scores(board, "2002") + self.scores(board, "2002"))
        eval -= 100 * (self.scores(board, "2020") + self.scores(board, "2020"))
        eval -= 100 * (self.scores(board, "0220") + self.scores(board, "0220"))
        eval -= 100 * (self.scores(board, "0202") + self.scores(board, "0202"))

        return eval


    def scores(self, board, player_win_str):
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            count = 0
            for row in b:
                if player_win_str in to_str(row):
                    count += 1
            return count

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int_)
                if player_win_str in to_str(root_diag):
                    count += 1

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int_))
                        if player_win_str in diag:
                            count += 1

            return count

        return (check_horizontal(board) +
                check_verticle(board) +
                check_diagonal(board))

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move


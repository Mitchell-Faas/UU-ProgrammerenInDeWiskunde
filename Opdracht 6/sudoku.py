import numpy as np
N = 2

class Sudoku():

    def __init__(self, n=2, board=None):
        if board is None:
            board = np.zeros(shape=(n ** 2, n ** 2), dtype=int)
            # Get input
            for i in range(n ** 2):
                # Note: Conversion to array and int happens implicitly here.
                board[i] = input().split()

        self.board = board
        self.n = n

    def solve_DFS(self, i=0, j=0):
        # If we have a solved board, return True.
        if not 0 in self.board:
            return True

        # Check if position is taken
        if self.board[i, j]:
            self.solve_DFS(i=i + (j + 1) // (self.n ** 2), j=(j + 1) % self.n ** 2)

        legal_options = self._legal_options(i, j)
        for num in legal_options:
            self.board[i, j] = num

            if self.solve_DFS(i=i + (j+1)//(self.n**2), j=(j+1) % self.n**2):
                return True
            self.board[i, j] = 0

        # If we have a solved board, return True.
        if not 0 in self.board:
            return True
        return False

    def print(self):
        for i in range(self.n**2):
            print(' '.join(map(str, self.board[i])))

    def make_move(self, num, row, col):
        self.board[row, col] = num

    def _legal_options(self, row, col):
        legal_options = []
        for n in range(1, self.n**2+1):
            if self._islegal(n, row, col):
                legal_options.append(n)
        return legal_options

    def _islegal(self, num, row, col):
        # Check if position is taken
        if self.board[row, col]:
            return False

        # Check if number exists in row or column
        if num in self.board[row,:] or num in self.board[:,col]:
            return False

        # Check if number exists in square
        row_sq_start = (row // self.n) * self.n
        col_sq_start = (col // self.n) * self.n
        if num in self.board[row_sq_start:row_sq_start+self.n, col_sq_start:col_sq_start+self.n]:
            return False

        return True

A = Sudoku()
if A.solve_DFS():
    A.print()
else:
    print("Unsolvable.")
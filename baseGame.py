import numpy as np

class Connect4:
    def __init__(self, rows=6, cols=7):
        if rows < 4 or cols < 4:
            raise ValueError("Board size must be at least 4x4")
        self.rows = rows
        self.cols = cols
        self.reset()

    def reset(self):
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.last_move = None
        return self.get_state()

    def get_state(self):
        return self.board.copy()

    def make_move(self, col):
        if self.game_over or not self.is_valid_move(col):
            return False, self.get_state(), -10, True

        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                break

        reward = self._check_winner(row, col)
        self.game_over = reward != 0 or len(self.get_valid_moves()) == 0
        self.current_player = 3 - self.current_player
        return True, self.get_state(), reward, self.game_over

    def _check_winner(self, row, col):
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i*dr, col + i*dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - i*dr, col - i*dc
                if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                self.winner = player
                return 1 if player == 1 else -1
        return 0

    def is_valid_move(self, col):
        return 0 <= col < self.cols and self.board[0][col] == 0 and not self.game_over

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def is_game_over(self):
        return self.game_over

    def render(self):
        for row in self.board:
            print("|" + "|".join([" " if cell == 0 else "X" if cell == 1 else "O" for cell in row]) + "|")
        print("-" * (2 * self.cols + 1))
        print(" " + " ".join([str(i) for i in range(self.cols)]))

    def __str__(self):
        return str(self.board)

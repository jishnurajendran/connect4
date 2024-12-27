#!/usr/bin/env python3
__all__ = ['Connect4']
# Connect-4 game, we consider a board of size n times n+1 for n>5
# we need a consice way to formulate the game,
# and best way to denote the board.
# 1. an empty board will have all zeros,
# 2. player 1 and player 2 move is denoted differently
# 3. the fist player with 4 connected pieces will win.
# Lets have a class, and this class is responsible for creating board, and the game.
# have a function to make the current player move.
# Make sure this class can act independent but also integrate well with pygame package for gui of game
# First we make the base game here.


class Connect4:
    def __init__(self, rows=6, cols=7):
        """Initialize the game board with customizable size"""
        if rows < 4 or cols < 4:
            raise ValueError("Board size must be at least 4x4")
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.last_move = None

    def make_move(self, col):
        """Make a move in the specified column"""
        if self.game_over or col < 0 or col >= self.cols:
            return False

        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                if self.check_winner(row, col):
                    self.game_over = True
                    self.winner = self.current_player
                elif self.is_board_full():
                    self.game_over = True
                else:
                    self.current_player = 3 - self.current_player
                return True
        return False

    def check_winner(self, row, col):
        """Check if the last move created a winning condition"""
        player = self.board[row][col]
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)], # Diagonal /
            [(1, -1), (-1, 1)]  # Diagonal \
        ]

        for dir_pair in directions:
            count = 1
            for direction in dir_pair:
                r, c = row, col
                dr, dc = direction
                while True:
                    r, c = r + dr, c + dc
                    if (0 <= r < self.rows and
                        0 <= c < self.cols and
                        self.board[r][c] == player):
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
        return False

    def is_valid_move(self, col):
        """Check if a move is valid in the specified column"""
        return (0 <= col < self.cols and
                self.board[0][col] == 0 and
                not self.game_over)

    def is_board_full(self):
        """Check if the board is full (draw)"""
        return all(self.board[0][col] != 0 for col in range(self.cols))

    def get_valid_moves(self):
        """Return a list of valid moves"""
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def get_board(self):
        """Return the current board state"""
        return [row[:] for row in self.board]

    def get_current_player(self):
        """Return the current player"""
        return self.current_player

    def is_game_over(self):
        """Return whether the game is over"""
        return self.game_over

    def get_winner(self):
        """Return the winner (None if no winner)"""
        return self.winner

    def get_last_move(self):
        """Return the last move made"""
        return self.last_move

    def reset(self):
        """Reset the game to initial state"""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.last_move = None

    def __str__(self):
        """Return a string representation of the board"""
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.board)

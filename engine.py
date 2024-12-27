from baseGame import Connect4

class Connect4Engine:
    def __init__(self):
        self.MAX_DEPTH = 2  # Maximum depth for minimax search
        self.WEIGHTS = {
            'win': 100000,
            'three_in_row': 100,
            'two_in_row': 10,
            'center_control': 3,
            'threat': -80,
            'block': 50
        }

    def evaluate_position(self, game, player):
        """Evaluate current board position"""
        if game.winner == player:
            return self.WEIGHTS['win']
        elif game.winner == 3 - player:
            return -self.WEIGHTS['win']
        elif game.is_board_full():
            return 0

        score = 0
        opponent = 3 - player

        # Center column control
        center_col = game.cols // 2
        center_count = sum(1 for row in range(game.rows) if game.board[row][center_col] == player)
        score += center_count * self.WEIGHTS['center_control']

        # Check horizontal windows
        for row in range(game.rows):
            for col in range(game.cols - 3):
                window = [game.board[row][col + i] for i in range(4)]
                score += self._evaluate_window(window, player)

        # Check vertical windows
        for row in range(game.rows - 3):
            for col in range(game.cols):
                window = [game.board[row + i][col] for i in range(4)]
                score += self._evaluate_window(window, player)

        # Check diagonal windows (positive slope)
        for row in range(game.rows - 3):
            for col in range(game.cols - 3):
                window = [game.board[row + i][col + i] for i in range(4)]
                score += self._evaluate_window(window, player)

        # Check diagonal windows (negative slope)
        for row in range(3, game.rows):
            for col in range(game.cols - 3):
                window = [game.board[row - i][col + i] for i in range(4)]
                score += self._evaluate_window(window, player)

        # Check threats
        for col in range(game.cols):
            if game.is_valid_move(col):
                # Try opponent's move
                game_copy = Connect4(game.rows)
                game_copy.board = [row[:] for row in game.board]
                game_copy.current_player = opponent
                game_copy.make_move(col)
                if game_copy.winner == opponent:
                    score += self.WEIGHTS['block']

        return score

    def _evaluate_window(self, window, player):
        """Evaluate a window of 4 positions"""
        opponent = 3 - player
        if window.count(player) == 4:
            return self.WEIGHTS['win']
        elif window.count(player) == 3 and window.count(0) == 1:
            return self.WEIGHTS['three_in_row']
        elif window.count(player) == 2 and window.count(0) == 2:
            return self.WEIGHTS['two_in_row']
        elif window.count(opponent) == 3 and window.count(0) == 1:
            return self.WEIGHTS['threat']
        return 0

    def get_best_move(self, game):
        """Get the best move for the current position"""
        best_score = float('-inf')
        best_move = None

        # Prioritize center early
        if sum(row.count(0) for row in game.board) >= game.rows * game.cols - 4:
            center_col = game.cols // 2
            if game.is_valid_move(center_col):
                return center_col

        # Try each possible move
        for col in range(game.cols):
            if game.is_valid_move(col):
                game_copy = Connect4(game.rows)
                game_copy.board = [row[:] for row in game.board]
                game_copy.current_player = game.current_player
                game_copy.make_move(col)
                score = self._minimax(game_copy, self.MAX_DEPTH - 1, False,
                                      float('-inf'), float('inf'), game.current_player)
                if score > best_score:
                    best_score = score
                    best_move = col

        return best_move

    def _minimax(self, game, depth, maximizing_player, alpha, beta, engine_player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or game.is_game_over():
            if game.winner == engine_player:
                return 1000
            elif game.winner == (3 - engine_player):
                return -1000
            elif game.is_board_full():
                return 0
            return self.evaluate_position(game, engine_player)

        if maximizing_player:
            max_eval = float('-inf')
            for col in range(game.cols):
                if game.is_valid_move(col):
                    game_copy = Connect4(game.rows)
                    game_copy.board = [row[:] for row in game.board]
                    game_copy.current_player = game.current_player
                    game_copy.make_move(col)
                    eval = self._minimax(game_copy, depth - 1, False, alpha, beta, engine_player)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(game.cols):
                if game.is_valid_move(col):
                    game_copy = Connect4(game.rows)
                    game_copy.board = [row[:] for row in game.board]
                    game_copy.current_player = game.current_player
                    game_copy.make_move(col)
                    eval = self._minimax(game_copy, depth - 1, True, alpha, beta, engine_player)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

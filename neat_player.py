import os
import neat
import pickle
import numpy as np
from baseGame import Connect4

class NEATPlayer:
    def __init__(self, config_file="connect4_config.txt", model_file="best_connect4_ai.pkl"):
        """Initialize NEAT player with saved model"""
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, config_file)

        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

        # Load the best network if it exists
        model_path = os.path.join(local_dir, model_file)
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                genome = pickle.load(f)
                self.network = neat.nn.FeedForwardNetwork.create(genome, self.config)
        else:
            raise FileNotFoundError(f"No trained model found at {model_file}")

    def get_board_state(self, game):
        """Convert board state to neural network input"""
        state = []
        for row in game.board:
            for cell in row:
                if cell == 0:
                    state.append(0.0)
                elif cell == 2:  # NEAT player is always player 2
                    state.append(1.0)
                else:
                    state.append(-1.0)

        # Add turn indicator (43rd input)
        state.append(1.0 if game.current_player == 2 else -1.0)

        return state

    def get_move(self, game):
        """Get the best move according to the NEAT network"""
        try:
            state = self.get_board_state(game)
            output = self.network.activate(state)

            valid_moves = [i for i in range(game.cols) if game.is_valid_move(i)]

            if not valid_moves:
                return None

            move_preferences = [(i, output[i]) for i in valid_moves]
            move_preferences.sort(key=lambda x: x[1], reverse=True)
            return move_preferences[0][0]

        except Exception as e:
            print(f"Error in NEAT move selection: {e}")
            return None

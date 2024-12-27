#!/usr/bin/env python3
import neat
import os
import pickle
from baseGame import Connect4
from engine import Connect4Engine
import random

class Connect4Trainer:
    def __init__(self):
        self.engine = Connect4Engine()
        self.training_games = 10  # Reduced for faster generations
        self.board_size = 6
        self.min_fitness = -1000

    def evaluate_genomes(self, genomes, config):
        """Evaluate all genomes"""
        print(f"Evaluating {len(genomes)} genomes...")

        for i, (genome_id, genome) in enumerate(genomes):
            if i % 10 == 0:  # Progress report every 10 genomes
                print(f"Evaluating genome {i}/{len(genomes)}")

            try:
                net = neat.nn.FeedForwardNetwork.create(genome, config)
                scores = []

                for game_num in range(self.training_games // 2):
                    # Play as player 1
                    game = Connect4(self.board_size)
                    score1 = self.play_game(game, net, 1)
                    scores.append(score1)

                    # Play as player 2
                    game = Connect4(self.board_size)
                    score2 = self.play_game(game, net, 2)
                    scores.append(score2)

                genome.fitness = sum(scores) / len(scores) if scores else self.min_fitness

            except Exception as e:
                print(f"Error evaluating genome {genome_id}: {e}")
                genome.fitness = self.min_fitness

        # Print best fitness of generation
        best_fitness = max(genome.fitness for _, genome in genomes)
        print(f"Best fitness in generation: {best_fitness}")

    def board_to_input(self, game, neat_player):
        """Convert board state to neural network input"""
        input_array = []

        # Convert board state to inputs
        for row in range(game.rows):
            for col in range(game.cols):
                value = game.board[row][col]
                if value == 0:
                    input_array.append(0.0)
                elif value == neat_player:
                    input_array.append(1.0)
                else:
                    input_array.append(-1.0)

        # Add turn indicator
        input_array.append(1.0 if game.current_player == neat_player else -1.0)

        return input_array

    def play_game(self, game, net, neat_player):
        """Play a single game"""
        engine_player = 3 - neat_player
        moves_made = 0
        max_moves = game.rows * game.cols

        while not game.is_game_over() and moves_made < max_moves:
            if game.current_player == neat_player:
                try:
                    inputs = self.board_to_input(game, neat_player)
                    outputs = net.activate(inputs)

                    valid_moves = [i for i in range(game.cols) if game.is_valid_move(i)]
                    if not valid_moves:
                        break

                    # Simple move selection - take the highest output for valid moves
                    move_scores = [(i, outputs[i]) for i in valid_moves]
                    best_move = max(move_scores, key=lambda x: x[1])[0]

                    if game.make_move(best_move):
                        moves_made += 1
                    else:
                        # Fallback to random move
                        move = random.choice(valid_moves)
                        game.make_move(move)
                        moves_made += 1

                except Exception as e:
                    # Make random move on error
                    valid_moves = [i for i in range(game.cols) if game.is_valid_move(i)]
                    if valid_moves:
                        move = random.choice(valid_moves)
                        game.make_move(move)
                        moves_made += 1
            else:
                # Engine's turn - limit thinking time
                try:
                    engine_move = self.engine.get_best_move(game)
                    if engine_move is not None and game.make_move(engine_move):
                        moves_made += 1
                    else:
                        break
                except:
                    # If engine fails, make random move
                    valid_moves = [i for i in range(game.cols) if game.is_valid_move(i)]
                    if valid_moves:
                        move = random.choice(valid_moves)
                        game.make_move(move)
                        moves_made += 1

        # Calculate score
        if game.winner == neat_player:
            return 100 + (42 - moves_made)  # Bonus for quick wins
        elif game.winner == engine_player:
            return -100
        return 0  # Draw

    def train(self, config_path):
        """Train the NEAT network"""
        try:
            # Load configuration
            config = neat.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                config_path
            )

            # Create population
            pop = neat.Population(config)

            # Add reporters
            pop.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            pop.add_reporter(stats)

            print("Starting evolution...")

            try:
                winner = pop.run(self.evaluate_genomes, 50)

                if winner:
                    print(f"Found winner with fitness: {winner.fitness}")
                    with open('best_connect4_ai.pkl', 'wb') as f:
                        pickle.dump(winner, f)
                    return winner
                else:
                    print("No winner found")
                    return None

            except Exception as e:
                print(f"Error during evolution: {e}")
                return None

        except Exception as e:
            print(f"Error in training: {e}")
            return None

def create_config():
    """Create the NEAT configuration file"""
    config_text = """[NEAT]
fitness_criterion     = max
fitness_threshold     = 400
pop_size             = 20
reset_on_extinction  = True
no_fitness_termination = True

[DefaultGenome]
# node activation options
activation_default      = tanh
activation_mutate_rate = 0.0
activation_options     = tanh

# node bias options
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
bias_max_value          = 30.0
bias_min_value          = -30.0
bias_mutate_power       = 0.5
bias_mutate_rate        = 0.7
bias_replace_rate       = 0.1

# node response options
response_init_mean      = 1.0
response_init_stdev     = 0.0
response_max_value      = 30.0
response_min_value      = -30.0
response_mutate_power   = 0.0
response_mutate_rate    = 0.0
response_replace_rate   = 0.0

# genome compatibility options
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# connection add/remove rates
conn_add_prob           = 0.5
conn_delete_prob        = 0.5

# connection enable options
enabled_default         = True
enabled_mutate_rate     = 0.01

# node add/remove rates
node_add_prob           = 0.2
node_delete_prob        = 0.2

# network parameters
num_inputs              = 43
num_hidden              = 4
num_outputs             = 7
initial_connection      = full_nodirect
feed_forward           = True

# connection weight options
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_max_value        = 30
weight_min_value        = -30
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
weight_replace_rate     = 0.1

# node aggregation options
aggregation_default     = sum
aggregation_mutate_rate = 0.0
aggregation_options     = sum

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation      = 15
species_elitism     = 2

[DefaultReproduction]
elitism            = 2
survival_threshold = 0.2
min_species_size   = 2"""

    with open('connect4_config.txt', 'w') as f:
        f.write(config_text)

if __name__ == "__main__":
    # Create config file if it doesn't exist
    create_config()

    # Get local directory path
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'connect4_config.txt')

    # Train the network
    trainer = Connect4Trainer()
    winner = trainer.train(config_path)
    if winner:
        print('\nBest genome:\n{!s}'.format(winner))
    else:
        print('\nTraining failed to produce a winner')

# Connect Four Game with NEAT AI

This project implements a Connect Four game with multiple AI opponents using Python, Pygame, and NEAT (NeuroEvolution of Augmenting Topologies). The game features various play modes and an evolving AI that learns to play Connect Four.

## Features

- Classic Connect Four gameplay
- Multiple game modes:
  - Human vs. Human
  - Human vs. AI (Minimax)
  - Human vs. NEAT AI
- NEAT-based AI that evolves with each generation

## Project Structure

The project consists of the following main components:

- `baseGame.py`: Implements the core Connect Four game logic
- `gameGUI.py`: Handles the game's graphical user interface
- `engine.py`: Contains the minimax AI engine
- `neat_player.py`: Implements the NEAT AI player
- `neat_trainer.py`: Trains the NEAT AI
- `connect4_config.txt`: Configuration file for NEAT

## Requirement 

Required dependencies:
   ```
   pip install pygame neat-python
   ```

## Usage

1. Train the NEAT AI (a pre-trained model is provided in `best_connect4_ai.pkl`):
   ```
   python neat_trainer.py
   ```

2. Run the game:
   ```
   python gameGUI.py
   ```

Use the mouse to select columns and drop pieces. Press 'R' to restart the game, 'Q' to quit, 'M' to change game modes, and 'E' to toggle AI evaluation display.

## AI Implementation

- The minimax AI uses alpha-beta pruning for efficient decision-making.
- The NEAT AI evolves neural networks to play Connect Four, improving over generations.

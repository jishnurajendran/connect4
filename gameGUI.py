#!/usr/bin/env python3

import pygame
import sys
from baseGame import Connect4
from engine import Connect4Engine
from neat_player import NEATPlayer

class Connect4GUI:
    # Colors
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    # Game modes
    HUMAN_VS_HUMAN = 0
    HUMAN_VS_ENGINE = 1
    HUMAN_VS_NEAT = 2

    def __init__(self, n, cell_size=100):
        """Initialize the GUI with board size n and cell size in pixels"""
        self.game = Connect4(n)
        self.cell_size = cell_size
        self.width = self.game.cols * cell_size
        self.height = (self.game.rows + 1) * cell_size  # Extra row for piece drop animation
        self.engine = Connect4Engine()
        self.game_mode = self.HUMAN_VS_HUMAN
        self.computer_player = 2
        self.show_eval = True
        self.neat_available = True

        # Initialize NEAT player
        try:
            self.neat_player = NEATPlayer()
        except FileNotFoundError:
            print("NEAT model not found. NEAT player mode will be disabled.")
            self.neat_player = None
            self.neat_available = False

        # Mode display text
        self.mode_texts = {
            self.HUMAN_VS_HUMAN: "Human vs Human",
            self.HUMAN_VS_ENGINE: "Human vs Engine",
            self.HUMAN_VS_NEAT: "Human vs NEAT" + (" (Not Available)" if not self.neat_available else "")
        }

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Connect 4')

        # Font for text
        self.font = pygame.font.Font(None, 74)

    def toggle_game_mode(self):
        """Cycle through game modes"""
        if self.neat_player is None:
            # If NEAT player is not available, only toggle between human and engine
            self.game_mode = self.HUMAN_VS_HUMAN if self.game_mode == self.HUMAN_VS_ENGINE else self.HUMAN_VS_ENGINE
        else:
            # Cycle through all modes
            self.game_mode = (self.game_mode + 1) % 3
        self.game.reset()

    def draw_evaluation(self):
        """Draw the engine's evaluation of the current position"""
        if not self.show_eval:
            return

        evaluation = self.engine.evaluate_position(self.game, self.game.current_player)

        eval_font = pygame.font.Font(None, 36)
        eval_text = f"Eval: {evaluation:+.1f}"

        eval_background = pygame.Surface((200, 30))
        eval_background.fill(self.WHITE)
        eval_background.set_alpha(230)

        if evaluation > 0:
            text_color = self.RED
        elif evaluation < 0:
            text_color = self.YELLOW
        else:
            text_color = self.BLACK

        eval_surface = eval_font.render(eval_text, True, text_color)

        background_rect = eval_background.get_rect(topright=(self.width - 10, 10))
        text_rect = eval_surface.get_rect(center=background_rect.center)

        self.screen.blit(eval_background, background_rect)
        self.screen.blit(eval_surface, text_rect)

    def draw_status(self):
        """Draw the game status text"""
        pygame.draw.rect(self.screen, self.WHITE,
                        (0, 0, self.width, self.cell_size))

        if self.game.is_game_over():
            if self.game.winner is not None:
                text = f"Player {self.game.winner} wins!"
                color = self.RED if self.game.winner == 1 else self.YELLOW
            else:
                text = "Game Draw!"
                color = self.BLACK
        else:
            text = f"Player {self.game.current_player}'s turn"
            color = self.RED if self.game.current_player == 1 else self.YELLOW

        instruction_font = pygame.font.Font(None, 26)
        instruction_text = "Press R to restart, Q to quit, M to change mode, E to toggle eval"
        mode_text = self.mode_texts[self.game_mode]

        # Add warning color for unavailable NEAT mode
        mode_color = self.BLACK
        if self.game_mode == self.HUMAN_VS_NEAT and not self.neat_available:
            mode_color = self.RED

        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(
            center=(self.width // 2, self.cell_size // 3))

        instruction_surface = instruction_font.render(instruction_text, True, self.BLACK)
        instruction_rect = instruction_surface.get_rect(
            center=(self.width // 2, self.cell_size * 2 // 3))

        mode_surface = instruction_font.render(mode_text, True, mode_color)
        mode_rect = mode_surface.get_rect(
            center=(self.width // 2, self.cell_size * 0.85))

        self.screen.blit(text_surface, text_rect)
        self.screen.blit(instruction_surface, instruction_rect)
        self.screen.blit(mode_surface, mode_rect)

    def draw_board(self):
        """Draw the game board"""
        self.screen.fill(self.WHITE)

        self.draw_status()
        self.draw_evaluation()

        # Draw the blue board
        pygame.draw.rect(self.screen, self.BLUE,
                        (0, self.cell_size, self.width, self.height - self.cell_size))

        # Draw cells
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                # Calculate center position for the circle
                center_x = col * self.cell_size + self.cell_size // 2
                center_y = (row + 1) * self.cell_size + self.cell_size // 2

                # Draw circle
                color = self.BLACK  # Empty cell
                if self.game.board[row][col] == 1:
                    color = self.RED  # Player 1
                elif self.game.board[row][col] == 2:
                    color = self.YELLOW  # Player 2

                pygame.draw.circle(self.screen, color,
                                 (center_x, center_y),
                                 self.cell_size // 2 - 5)

        # Draw the hovering piece in the top row
        if not self.game.is_game_over():
            mouse_x = pygame.mouse.get_pos()[0]
            col = mouse_x // self.cell_size
            if 0 <= col < self.game.cols:
                color = self.RED if self.game.current_player == 1 else self.YELLOW
                pygame.draw.circle(self.screen, color,
                                 (col * self.cell_size + self.cell_size // 2,
                                  self.cell_size // 2),
                                 self.cell_size // 2 - 5)

        pygame.display.update()

    def show_winner_message(self):
        """This method is now handled by draw_status"""
        pass

    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game.is_game_over():
                    mouse_x = event.pos[0]
                    col = mouse_x // self.cell_size

                    if self.game.make_move(col):
                        if self.game.is_game_over():
                            self.draw_board()
                        elif self.game_mode != self.HUMAN_VS_HUMAN and self.game.current_player == self.computer_player:
                            computer_move = None
                            if self.game_mode == self.HUMAN_VS_ENGINE:
                                computer_move = self.engine.get_best_move(self.game)
                            elif self.game_mode == self.HUMAN_VS_NEAT and self.neat_player:
                                computer_move = self.neat_player.get_move(self.game)

                            if computer_move is not None:
                                self.game.make_move(computer_move)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game with 'R' key
                        self.game.reset()
                    elif event.key == pygame.K_q:  # Quit with 'Q' key
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_m:  # Toggle game mode
                        self.toggle_game_mode()
                    elif event.key == pygame.K_e:  # Toggle evaluation display
                        self.show_eval = not self.show_eval

            self.draw_board()
            pygame.time.wait(50)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    # Create and run the game with a 6x7 board
    gui_game = Connect4GUI(6)
    gui_game.run()

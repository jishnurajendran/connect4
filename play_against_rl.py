import torch
import numpy as np
from baseGame import Connect4
from RL_agent import DQN, DQNAgent

def load_trained_agent(model_path):
    env = Connect4()
    state_size = env.rows * env.cols
    action_size = env.cols
    agent = DQNAgent(state_size, action_size)
    agent.policy_net.load_state_dict(torch.load(model_path))
    agent.policy_net.eval()
    return agent

def play_against_rl():
    env = Connect4()
    agent = load_trained_agent("connect4_dqn.pth")

    while True:
        env.reset()
        done = False
        while not done:
            env.render()
            if env.current_player == 1:
                while True:
                    try:
                        move = int(input("Enter your move (0-6): "))
                        if env.is_valid_move(move):
                            break
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number between 0 and 6.")
            else:
                state = np.array(env.get_state()).flatten()
                valid_moves = env.get_valid_moves()
                move = agent.get_action(state, valid_moves)

            _, reward, done, _ = env.make_move(move)

        env.render()
        if env.winner == 1:
            print("You win!")
        elif env.winner == 2:
            print("RL agent wins!")
        else:
            print("It's a draw!")

        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    play_against_rl()

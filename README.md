# Two Snake Q-Learning Simulation

This project implements a simulation of two snakes learning to navigate and compete for food using Q-learning, a reinforcement learning algorithm.

## Description

In this simulation, two snakes independently learn to navigate a grid-based environment, avoid walls, and collect food. The snakes use Q-learning to improve their decision-making over time, with their learned behaviors persisting across multiple games and program executions.

## Features

- Two snakes controlled by separate Q-learning algorithms
- Persistent learning across multiple games and program executions
- Visual representation of the snakes and food using Pygame
- Option to restart the game or exit after a snake dies
- Terminal output for tracking game progress and snake scores

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required packages:
```bash
pip install pygame numpy
```
3. Download the `game.py` file to your local machine.

## Usage

1. Run the program:
```bash
python3 game.py
```
2. Observe the snakes as they learn and navigate the environment.

3. When a snake dies:

- Press Enter to restart the game with updated Q-tables
- Press Spacebar to exit the program

## How It Works

- Each snake has a Q-table that stores the expected rewards for actions in different states.
- The snakes learn by updating their Q-tables based on the rewards they receive for their actions.
- The learning persists across games, allowing the snakes to improve their strategies over time.
- The epsilon parameter balances exploration (random actions) and exploitation (using learned values).

## Customization

You can modify various parameters in the code to experiment with different learning scenarios:
- Grid size and game speed
- Learning parameters (epsilon, alpha, gamma)
- Reward structure

## Contributing

Feel free to fork this project and submit pull requests with improvements or additional features.

## License

This project is open source and available under the .

## Contact 

avijit.dhaliwal@gmail.com
import pygame
import random
import numpy as np
import pickle

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 10
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Snake Q-Learning")

class Snake:
    def __init__(self, x, y, color, name):
        self.body = [(x, y)]
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.color = color
        self.score = 0
        self.name = name
        self.q_table = np.zeros((GRID_WIDTH, GRID_HEIGHT, 4, 3))  # 4 directions, 3 actions

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            return False
        
        self.body.insert(0, new_head)
        if len(self.body) > self.score + 1:
            self.body.pop()
        return True

    def grow(self):
        self.score += 1

    def get_state(self):
        head = self.body[0]
        direction_index = [(1, 0), (0, 1), (-1, 0), (0, -1)].index(self.direction)
        return (head[0], head[1], direction_index)

    def choose_action(self, epsilon):
        if random.random() < epsilon:
            return random.randint(0, 2)  # 0: forward, 1: left, 2: right
        else:
            state = self.get_state()
            return np.argmax(self.q_table[state])

    def update_direction(self, action):
        # 0: forward, 1: left, 2: right
        if action == 1:  # Turn left
            self.direction = (self.direction[1], -self.direction[0])
        elif action == 2:  # Turn right
            self.direction = (-self.direction[1], self.direction[0])

    def update_q_table(self, state, action, reward, new_state, alpha, gamma):
        old_value = self.q_table[state][action]
        next_max = np.max(self.q_table[new_state])
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        self.q_table[state][action] = new_value

def create_food():
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

def calculate_reward(snake, food):
    head = snake.body[0]
    distance = abs(head[0] - food[0]) + abs(head[1] - food[1])
    if head == food:
        return 10
    elif head[0] == 0 or head[0] == GRID_WIDTH - 1 or head[1] == 0 or head[1] == GRID_HEIGHT - 1:
        return -5
    else:
        return 1 / (distance + 1)

def save_q_tables(snake1, snake2):
    with open('snake1_q_table.pkl', 'wb') as f:
        pickle.dump(snake1.q_table, f)
    with open('snake2_q_table.pkl', 'wb') as f:
        pickle.dump(snake2.q_table, f)

def load_q_tables():
    try:
        with open('snake1_q_table.pkl', 'rb') as f:
            snake1_q_table = pickle.load(f)
        with open('snake2_q_table.pkl', 'rb') as f:
            snake2_q_table = pickle.load(f)
        return snake1_q_table, snake2_q_table
    except FileNotFoundError:
        return None, None

def game_loop():
    # Load Q-tables if they exist
    snake1_q_table, snake2_q_table = load_q_tables()

    # Initialize snakes and food
    snake1 = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, GREEN, "Snake 1")
    snake2 = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, YELLOW, "Snake 2")
    
    if snake1_q_table is not None:
        snake1.q_table = snake1_q_table
    if snake2_q_table is not None:
        snake2.q_table = snake2_q_table

    food = create_food()

    # Q-learning parameters
    epsilon = 0.1
    alpha = 0.1
    gamma = 0.9

    clock = pygame.time.Clock()
    running = True
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        step += 1
        print(f"\nStep {step}")

        for snake in [snake1, snake2]:
            state = snake.get_state()
            action = snake.choose_action(epsilon)
            snake.update_direction(action)
            
            if not snake.move():
                print(f"{snake.name} hit a wall! Game over.")
                print("Press Enter to restart or Spacebar to exit.")
                save_q_tables(snake1, snake2)
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                return True  # Restart the game
                            elif event.key == pygame.K_SPACE:
                                return False  # Exit the program
                break

            if snake.body[0] == food:
                snake.grow()
                print(f"{snake.name} ate food! Score: {snake.score}")
                food = create_food()

            new_state = snake.get_state()
            reward = calculate_reward(snake, food)
            snake.update_q_table(state, action, reward, new_state, alpha, gamma)

        # Drawing code
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for snake in [snake1, snake2]:
            for segment in snake.body:
                pygame.draw.rect(screen, snake.color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.display.flip()
        clock.tick(10)  # Slower speed for better observation

    print(f"\nFinal Scores:")
    print(f"Snake 1: {snake1.score}")
    print(f"Snake 2: {snake2.score}")
    save_q_tables(snake1, snake2)
    return False

# Main program loop
while True:
    if not game_loop():
        break

pygame.quit()
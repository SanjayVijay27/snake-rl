import random
#from unicodedata import name
import pygame
from enum import Enum
from collections import namedtuple
import numpy as np
import math

pygame.init()

# make a map, the snake, and the fruit
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x , y")

BLOCK_SIZE = 20
SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.Font(pygame.font.get_default_font(), 24)

class SnakeAI:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2 * BLOCK_SIZE, self.head.y),
        ]
        self.food = None
        self.score = 0

        self.place_food()
        self.frame_iteration = 0

    def place_food(self):
        self.food = Point(
            BLOCK_SIZE * random.randint(0, self.width / BLOCK_SIZE - 1),
            BLOCK_SIZE * random.randint(0, self.height / BLOCK_SIZE - 1),
        )
        if self.food in self.snake:
            self.place_food()

    def move(self, action):
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clockwise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clockwise[index]
        elif np.array_equal(action, [0, 1, 0]):
            next_index = (index + 1) % 4    #turn right
            new_dir = clockwise[next_index]
        elif np.array_equal(action, [0, 0, 1]):
            next_index = (index - 1) % 4    #turn left
            new_dir = clockwise[next_index]
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.width - BLOCK_SIZE or pt.x < 0 or pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True
        return pt in self.snake[1:]

    def update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                self.display, GREEN, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)
            )
        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )
        text = FONT.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.move(action)
        self.snake.insert(0, self.head)
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()
        self.update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score

    # movement of snake, collision of snake, UI update, function to play game
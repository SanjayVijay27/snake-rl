import random
#from unicodedata import name
import pygame
from enum import Enum
from collections import namedtuple

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

class Snake:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
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

    def place_food(self):
        self.food = Point(
            BLOCK_SIZE * random.randint(0, self.width / BLOCK_SIZE - 1),
            BLOCK_SIZE * random.randint(0, self.height / BLOCK_SIZE - 1),
        )
        if self.food in self.snake:
            self.place_food()

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def collision(self):
        return (
            self.head.x <= 0 - BLOCK_SIZE
            or self.head.x >= self.width
            or self.head.y <= 0 - BLOCK_SIZE
            or self.head.y >= self.height
            or self.head in self.snake[1:]
        )

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

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        self.move(self.direction)
        self.snake.insert(0, self.head)
        game_over = False
        if self.collision():
            game_over = True
            return game_over, self.score
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()
        self.update_ui()
        self.clock.tick(SPEED)
        return game_over, self.score

    # movement of snake, collision of snake, UI update, function to play game


if __name__ == "__main__":
    game = Snake()
    while True:
        game_over, score = game.play_step()
        if game_over:
            break
    print(score)
    pygame.quit()
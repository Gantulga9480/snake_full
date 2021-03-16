import pygame
import numpy as np
import math as mt
from utils import *
from snake_brain import Brain


def init():
    pygame.init()
    pygame.display.set_caption("SNAKE")


class Snake:

    def __init__(self):
        init()
        self.font = pygame.font.SysFont("arial", 25)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_flip = True
        self.run = True
        self.score = 0
        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        self.snake = list()
        self.food_x = 0
        self.food_y = 0
        self.out = False
        self.over = False
        self.food_hit = False
        self.brain = Brain()

    def step(self):
        if self.game_flip:
            self.draw_game(self.board)
        self.handle_event()
        action = self.brain.move(self.snake[0].copy(),
                                 self.snake[-1].copy(),
                                 self.board.copy(),
                                 [self.food_x, self.food_y])
        for i, block in reversed(list(enumerate(self.snake))):
            if i == 0:
                self.get_action_dir(action)
                print(self.snake[0][2])
            else:
                block[2] = self.snake[i-1][2]
            self.snake[i] = self.draw_snake(block, i)
        self.food_check()

    def feedback(self):
        pass

    def get_dis(self):
        diff_x = self.food_x - self.snake[0][0]
        diff_y = self.food_y - self.snake[0][1]
        dis = mt.sqrt((diff_x**2 + diff_y**2))
        return dis

    def get_action_dir(self, action):
        self.snake[0][2] = action

    def get_possible_actions(self):
        if self.snake[0][2] == "↑":
            return (0, 1, 3), 2
        elif self.snake[0][2] == "→":
            return (0, 1, 2), 3
        elif self.snake[0][2] == "↓":
            return (1, 2, 3), 0
        elif self.snake[0][2] == "←":
            return (0, 2, 3), 1

    def reset(self):
        self.over = False
        self.out = False
        self.score = 0
        self.snake.clear()
        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        d = np.random.randint(1, 5)
        if d == 1:
            ldir = "↓"
            x = np.random.randint(2, BOARD_COUNT - 1)
            x_1 = x - 1
            x_2 = x_1 - 1
            y = np.random.randint(0, BOARD_COUNT - 1)
            y_1 = y
            y_2 = y_1
        elif d == 2:
            ldir = "→"
            y = np.random.randint(2, BOARD_COUNT - 1)
            y_1 = y - 1
            y_2 = y_1 - 1
            x = np.random.randint(0, BOARD_COUNT - 1)
            x_1 = x
            x_2 = x_1
        elif d == 3:
            ldir = "↑"
            x = np.random.randint(0, BOARD_COUNT - 3)
            x_1 = x + 1
            x_2 = x_1 + 1
            y = np.random.randint(0, BOARD_COUNT - 1)
            y_1 = y
            y_2 = y_1
        elif d == 4:
            ldir = "←"
            x = np.random.randint(0, BOARD_COUNT - 1)
            x_1 = x
            x_2 = x_1
            y = np.random.randint(0, BOARD_COUNT - 3)
            y_1 = y + 1
            y_2 = y_1 + 1
        self.board[x][y] = HEAD
        self.board[x_1][y_1] = TAIL
        self.board[x_2][y_2] = TAIL
        self.snake.append([x, y, ldir])
        self.snake.append([x_1, y_1, ldir])
        self.snake.append([x_2, y_2, ldir])
        self.create_food()

    def draw_snake(self, block_s, index):
        x = block_s[0]
        y = block_s[1]
        if block_s[2] == "↑":
            if index == 0:
                if x == 0 or self.board[x-1][y] == TAIL:
                    self.out = True
                else:
                    self.board[x-1][y] = HEAD
                    block_s[0] -= 1
            else:
                self.board[x-1][y] = TAIL
                block_s[0] -= 1
        elif block_s[2] == "↓":
            if index == 0:
                if x == BOARD_COUNT - 1 or self.board[x+1][y] == TAIL:
                    self.out = True
                else:
                    self.board[x+1][y] = HEAD
                    block_s[0] += 1
            else:
                self.board[x+1][y] = TAIL
                block_s[0] += 1
        elif block_s[2] == "←":
            if index == 0:
                if y == 0 or self.board[x][y-1] == TAIL:
                    self.out = True
                else:
                    self.board[x][y-1] = HEAD
                    block_s[1] -= 1
            else:
                self.board[x][y-1] = TAIL
                block_s[1] -= 1
        elif block_s[2] == "→":
            if index == 0:
                if y == BOARD_COUNT - 1 or self.board[x][y+1] == TAIL:
                    self.out = True
                else:
                    self.board[x][y+1] = HEAD
                    block_s[1] += 1
            else:
                self.board[x][y+1] = TAIL
                block_s[1] += 1
        if index == len(self.snake) - 1:
            self.board[x][y] = 0
        return block_s

    def draw_game(self, board):
        self.win.fill((0, 0, 0))
        pygame.draw.line(self.win, WHITE,
                         (20, 20),
                         (20, 520))
        pygame.draw.line(self.win, WHITE,
                         (20 + BOARD_COUNT * VELOCITY, 20),
                         (20 + BOARD_COUNT * VELOCITY, 520))
        pygame.draw.line(self.win, WHITE,
                         (20, 20),
                         (520, 20))
        pygame.draw.line(self.win, WHITE,
                         (20, 20 + BOARD_COUNT * VELOCITY),
                         (520, 20 + BOARD_COUNT * VELOCITY))
        score_str = self.font.render(f"Score: {self.score}", 1, WHITE)
        self.win.blit(score_str, (240, 540))
        for i, item in enumerate(self.snake):
            if i == 0:
                pygame.draw.rect(self.win, YELLOW,
                                 (VELOCITY*item[1]+21, VELOCITY*item[0]+21,
                                  SHAPE, SHAPE))
            else:
                pygame.draw.rect(self.win, RED,
                                 (VELOCITY*item[1]+21, VELOCITY*item[0]+21,
                                  SHAPE, SHAPE))
        pygame.draw.rect(self.win, GREEN,
                         (VELOCITY*self.food_y+21, VELOCITY*self.food_x+21,
                          SHAPE, SHAPE))
        pygame.display.flip()
        self.clock.tick(FPS)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.over = True
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_flip:
                        self.game_flip = True
                    elif self.game_flip:
                        self.game_flip = False
                elif event.key == pygame.K_r:
                    self.over = True
                elif event.key == pygame.K_UP:
                    FPS += 1
                elif event.key == pygame.K_DOWN:
                    FPS -= 1

    def create_food(self):
        while True:
            counter = 0
            self.food_x = np.random.randint(0, BOARD_COUNT - 1)
            self.food_y = np.random.randint(0, BOARD_COUNT - 1)
            blocks = [[self.food_x - 1, self.food_y],
                      [self.food_x, self.food_y - 1],
                      [self.food_x + 1, self.food_y],
                      [self.food_x, self.food_y + 1]]
            if self.board[self.food_x, self.food_y] == EMPTY:
                for item in blocks:
                    if self.board[item[0]][item[1]] == EMPTY:
                        counter += 1
                    else:
                        pass
                if counter >= 0:
                    self.board[self.food_x][self.food_y] = FOOD
                    break

    def add_tail(self):
        tail = self.snake[-1].copy()
        if tail[2] == "↑":
            tail[0] += 1
        elif tail[2] == "↓":
            tail[0] -= 1
        elif tail[2] == "←":
            tail[1] += 1
        elif tail[2] == "→":
            tail[1] -= 1
        if self.board[tail[0], tail[1]] != EMPTY:
            print("Can't add tail")
            print(self.snake[0])
            print(tail)
            print(self.food_x, self.food_y)
            print(self.board)
            quit()
        self.board[tail[0]][tail[1]] = TAIL
        self.snake.append(tail)

    def food_check(self):
        if self.snake[0][0] == self.food_x and self.snake[0][1] == self.food_y:
            self.food_hit = True
            self.score += 1
            self.add_tail()
            self.create_food()

    @staticmethod
    def caption(msg):
        pygame.display.set_caption(msg)

    def check_snake(self):
        for i, item in enumerate(self.snake):
            for j, item_j in enumerate(self.snake):
                if i == j:
                    pass
                else:
                    if item[0] == item_j[0] and item[1] == item_j[1]:
                        print("Snake broke")
                        print(self.snake)
                        print(self.board)
                        quit()

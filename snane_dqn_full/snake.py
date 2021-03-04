import pygame
import numpy as np
import math as mt
from utils import *


def init():
    pygame.init()
    pygame.display.set_caption("SNAKE")


class Snake:

    def __init__(self, test=False):
        init()
        self.fps = FPS
        if test:
            self.vel = TEST_VEL
            self.shape = TEST_SHAPE
            self.board_count = TEST_BOARD_COUNT
        else:
            self.vel = VELOCITY
            self.shape = SHAPE
            self.board_count = BOARD_COUNT
        self.font = pygame.font.SysFont("arial", 25)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_flip = True
        self.run = True
        self.debug = False
        self.score = 0

        self.board = np.zeros((self.board_count, self.board_count), dtype=int)
        self.snake = list()
        self.food_x = 0
        self.food_y = 0
        self.out = False
        self.over = False
        self.food_hit = False
        self.save = False

    def step(self, action=None):
        if self.game_flip:
            self.draw_game(self.board)
        self.handle_event()
        for i, block in reversed(list(enumerate(self.snake))):
            if i == 0:
                self.get_action_dir(action)
            else:
                block[2] = self.snake[i-1][2]
            self.snake[i] = self.snake_step(block, i)
        self.food_check()
        return self.feedback()

    def feedback(self):
        if self.out:
            self.over = True
            return self.over, self.get_state(), OUT_REWARD
        elif self.food_hit:
            self.food_hit = False
            self.score = len(self.snake) - 3
            return self.over, self.get_state(), self.score
        else:
            return self.over, self.get_state(), EMPTY_STEP_REWARD

    def get_state(self):
        return self.board.flatten()
        return self.get_window()

    def reward_func(self):
        return EMPTY_STEP_REWARD

    def get_window(self):
        x = self.snake[0][0]
        y = self.snake[0][1]
        state = []
        dis_x = self.food_x - x
        dis_y = self.food_y - y
        # state = [dis_x, dis_y]
        if dis_x < 0 and dis_y < 0:
            state.append(0)
        elif dis_x < 0 and dis_y == 0:
            state.append(1)
        elif dis_x < 0 and dis_y > 0:
            state.append(2)
        elif dis_x == 0 and dis_y > 0:
            state.append(3)
        elif dis_x > 0 and dis_y > 0:
            state.append(4)
        elif dis_x > 0 and dis_y == 0:
            state.append(5)
        elif dis_x > 0 and dis_y < 0:
            state.append(6)
        elif dis_x == 0 and dis_y < 0:
            state.append(7)
        elif dis_x == 0 and dis_y == 0:
            print('wrong state')
            quit()
        win_x = self.snake[0][0]
        win_y = self.snake[0][1]
        end_x = win_x + WINDOW_SIZE
        end_y = win_y + WINDOW_SIZE
        board = np.pad(self.board, WINDOW_SIZE//2)
        board = board[win_x:end_x, win_y:end_y]
        board = board.flatten()
        state = np.array(state)
        states = np.concatenate((state, board), axis=0)
        return states

    def get_action_dir(self, action):
        if action == 0:
            self.snake[0][2] = "↑"
        elif action == 1:
            self.snake[0][2] = "→"
        elif action == 2:
            self.snake[0][2] = "↓"
        elif action == 3:
            self.snake[0][2] = "←"

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
        self.board = np.zeros((self.board_count, self.board_count), dtype=int)
        d = np.random.randint(1, 5)
        if d == 1:
            ldir = "↓"
            x = np.random.randint(2, self.board_count - 1)
            x_1 = x - 1
            x_2 = x_1 - 1
            y = np.random.randint(0, self.board_count - 1)
            y_1 = y
            y_2 = y_1
        elif d == 2:
            ldir = "→"
            y = np.random.randint(2, self.board_count - 1)
            y_1 = y - 1
            y_2 = y_1 - 1
            x = np.random.randint(0, self.board_count - 1)
            x_1 = x
            x_2 = x_1
        elif d == 3:
            ldir = "↑"
            x = np.random.randint(0, self.board_count - 3)
            x_1 = x + 1
            x_2 = x_1 + 1
            y = np.random.randint(0, self.board_count - 1)
            y_1 = y
            y_2 = y_1
        elif d == 4:
            ldir = "←"
            x = np.random.randint(0, self.board_count - 1)
            x_1 = x
            x_2 = x_1
            y = np.random.randint(0, self.board_count - 3)
            y_1 = y + 1
            y_2 = y_1 + 1
        self.board[x][y] = HEAD
        self.board[x_1][y_1] = TAIL
        self.board[x_2][y_2] = TAIL
        self.snake.append([x, y, ldir])
        self.snake.append([x_1, y_1, ldir])
        self.snake.append([x_2, y_2, ldir])
        self.create_food()
        return self.get_state()

    def snake_step(self, block_s, index):
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
                if x == self.board_count - 1 or self.board[x+1][y] == TAIL:
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
                if y == self.board_count - 1 or self.board[x][y+1] == TAIL:
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
                         (20 + self.board_count * self.vel, 20),
                         (20 + self.board_count * self.vel, 520))
        pygame.draw.line(self.win, WHITE,
                         (20, 20),
                         (520, 20))
        pygame.draw.line(self.win, WHITE,
                         (20, 20 + self.board_count * self.vel),
                         (520, 20 + self.board_count * self.vel))
        score_str = self.font.render(f"Score: {self.score}", 1, WHITE)
        self.win.blit(score_str, (240, 540))
        food_drawn = False
        for i in range(self.board_count):
            for j in range(self.board_count):
                if board[i][j] == HEAD:
                    pygame.draw.rect(self.win, YELLOW,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
                elif board[i][j] == TAIL:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
                elif board[i][j] == FOOD:
                    food_drawn = True
                    pygame.draw.rect(self.win, GREEN,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
        # self.draw_win()
        pygame.display.flip()
        self.clock.tick(self.fps)
        if not food_drawn:
            print('[WARNING FOOD NOT FOUND]', self.food_hit)

    def draw_win(self):
        win_x = self.snake[0][0] - WINDOW_SIZE//2
        win_y = self.snake[0][1] - WINDOW_SIZE//2
        end_x = win_x + WINDOW_SIZE
        end_y = win_y + WINDOW_SIZE
        pygame.draw.line(self.win, WHITE,
                         (win_y*self.vel+21, win_x*self.vel+21),
                         (win_y*self.vel+21, end_x*self.vel+21))
        pygame.draw.line(self.win, WHITE,
                         (win_y*self.vel+21, win_x*self.vel+21),
                         (end_y*self.vel+21, win_x*self.vel+21))
        pygame.draw.line(self.win, WHITE,
                         (end_y*self.vel+21, win_x*self.vel+21),
                         (end_y*self.vel+21, end_x*self.vel+21))
        pygame.draw.line(self.win, WHITE,
                         (win_y*self.vel+21, end_x*self.vel+21),
                         (end_y*self.vel+21, end_x*self.vel+21))

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
                    self.fps += 1
                elif event.key == pygame.K_DOWN:
                    self.fps -= 1
                elif event.key == pygame.K_s:
                    self.save = True

    def create_food(self):
        while True:
            counter = 0
            self.food_x = np.random.randint(0, self.board_count - 1)
            self.food_y = np.random.randint(0, self.board_count - 1)
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
                if counter >= 2:
                    self.board[self.food_x, self.food_y] = FOOD
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

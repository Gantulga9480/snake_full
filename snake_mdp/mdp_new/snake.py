import pygame
import numpy as np
import math as mt
from utils import *
import snake_table as st


def init(status):
    pygame.init()
    status = status if status is not None else ""
    pygame.display.set_caption(f"SNAKE {status}")


class Snake:

    def __init__(self, colorful=False, num=False, update_rate=1):
        self.fps = FPS
        self.colorful = colorful
        self.num = num
        self.update_rate = update_rate if update_rate is not None else 1
        self.vel = VELOCITY
        self.shape = SHAPE
        font_size = np.int(SHAPE - np.sqrt(2*(SHAPE/3)**2))
        self.font1 = pygame.font.SysFont("arial", font_size)
        self.font = pygame.font.SysFont("arial", 25)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_flip = True
        self.run = True
        self.debug = False

        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        self.snake = list()
        self.food_x = 0
        self.food_y = 0
        self.dis_diff = 0
        self.out = False
        self.over = False
        self.food_hit = False
        self.win_state = {}

        self.v = st.ValueFunction(update_rate=self.update_rate)

    def step(self, action=None):
        # self.check_snake()
        self.caption(f'{self.update_rate}')
        if self.game_flip:
            self.draw_game(self.board)
        self.handle_event()
        for i, block in reversed(list(enumerate(self.snake))):
            if i == 0:
                self.get_action_dir(action)
            else:
                block[2] = self.snake[i-1][2]
            self.snake[i] = self.draw_snake(block, i)
        self.food_check()
        return self.feedback()

    def feedback(self):
        if self.out:
            self.over = True
            return self.over, self.get_state(), OUT_REWARD
        elif self.food_hit:
            self.food_hit = False
            self.v.reset(self.board.copy())
            return self.over, self.get_state(), FOOD_REWARD
        else:
            self.v.update(self.board.copy(), ur=self.update_rate)
            return self.over, self.get_state(), EMPTY_STEP_REWARD

    def get_state(self):
        return [self.snake[0][0], self.snake[0][1]]

    def get_action_dir(self, action):
        if action == 0:
            self.snake[0][2] = "↑"
        elif action == 1:
            self.snake[0][2] = "↓"
        elif action == 2:
            self.snake[0][2] = "←"
        elif action == 3:
            self.snake[0][2] = "→"

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
        self.v.reset(self.board.copy())
        return self.get_state()

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
        self.score = len(self.snake) - 3
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
        food_drawn = False
        for i in range(BOARD_COUNT):
            for j in range(BOARD_COUNT):
                score = self.v.table[i][j]
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
                else:
                    if self.colorful:
                        if score < 0:
                            if np.abs(score)/FOOD_REWARD >= 1:
                                pygame.draw.rect(self.win, BLUE,
                                                 (self.vel*j+21, self.vel*i+21,
                                                  self.shape, self.shape))
                            else:
                                color = 1 - np.abs(score)/FOOD_REWARD
                                pygame.draw.rect(self.win, (255*color,
                                                            255*color,
                                                            255),
                                                 (self.vel*j+21, self.vel*i+21,
                                                  self.shape, self.shape))
                        elif score == 0:
                            pygame.draw.rect(self.win, WHITE,
                                             (self.vel*j+21, self.vel*i+21,
                                              self.shape, self.shape))
                        else:
                            color = 1 - score/FOOD_REWARD
                            pygame.draw.rect(self.win, (255*color,
                                                        255,
                                                        255*color),
                                             (self.vel*j+21, self.vel*i+21,
                                              self.shape, self.shape))
                if self.num:
                    if 0 < np.abs(score)-np.floor(np.abs(score)) < 1:
                        string1 = f"{np.round(score, 2)}"
                    else:
                        string1 = f"{int(score)}"
                    s = self.font1.render(string1, 1, BLACK)
                    self.win.blit(s, (j*self.vel + 26, i*self.vel + 26))
        pygame.display.flip()
        self.clock.tick(self.fps)
        if not food_drawn:
            print('[WARNING FOOD NOT FOUND]', self.food_hit)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_flip:
                        self.game_flip = True
                    elif self.game_flip:
                        self.game_flip = False
                elif event.key == pygame.K_DOWN:
                    self.fps -= 2
                elif event.key == pygame.K_UP:
                    self.fps += 2
                elif event.key == pygame.K_LEFT:
                    self.update_rate += 1
                elif event.key == pygame.K_RIGHT:
                    self.update_rate -= 1
                elif event.key == pygame.K_c:
                    if self.colorful:
                        self.colorful = False
                    else:
                        self.colorful = True
                elif event.key == pygame.K_v:
                    if self.num:
                        self.num = False
                    else:
                        self.num = True

    def create_food(self):
        while True:
            counter = 0
            self.food_x = np.random.randint(0, BOARD_COUNT - 1)
            self.food_y = np.random.randint(0, BOARD_COUNT - 1)
            if self.board[self.food_x, self.food_y] == EMPTY:
                blocks = [[self.food_x-1, self.food_y],
                          [self.food_x, self.food_y + 1],
                          [self.food_x+1, self.food_y],
                          [self.food_x, self.food_y-1]]
                for item in blocks:
                    try:
                        if self.board[item[0], item[1]] == EMPTY:
                            counter += 1
                    except IndexError:
                        pass
                if counter == 4:
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

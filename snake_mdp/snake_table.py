import numpy as np
from utils import *


class ValueFunction:

    def __init__(self, update_rate):
        self.gamma = 0.9
        self.update_rate = update_rate

    def reset(self, board):
        self.init_table(board)
        self.update(board, reset=True)

    def update(self, board, reset=False, ur=None):
        if ur is None:
            pass
        else:
            self.update_rate = ur
        start_table = self.table.copy()
        temp_value = start_table.copy()
        if reset:
            itr = self.update_rate
        else:
            itr = 1
        for _ in range(itr):
            for i in range(BOARD_COUNT):
                for j in range(BOARD_COUNT):
                    if board[i][j] == TAIL:
                        temp_value[i][j] = OUT_REWARD
                    elif board[i][j] == FOOD:
                        temp_value[i][j] = FOOD_REWARD
                    else:
                        temp_value[i][j] = self.getStateVal([i, j])
            self.table = temp_value.copy()

    def getAction(self, state):
        next_state = [[state[0]-1, state[1]], [state[0]+1, state[1]],
                      [state[0], state[1]-1], [state[0], state[1]+1]]
        vals = []
        for _, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(self.table[item[0]][item[1]])
                else:
                    vals.append(OUT_REWARD)
            except IndexError:
                vals.append(OUT_REWARD)
        return np.argmax(vals)

    def getStateVal(self, state):
        next_state = [[state[0]-1, state[1]], [state[0], state[1]+1],
                      [state[0], state[1]-1], [state[0]+1, state[1]]]
        vals = []
        for _, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(EMPTY_STEP_REWARD +
                                self.gamma * self.table[item[0]][item[1]])
                else:
                    pass
            except IndexError:
                pass
        return max(vals)

    def init_table(self, board):
        self.table = np.zeros((BOARD_COUNT, BOARD_COUNT))
        for i in range(BOARD_COUNT):
            for j in range(BOARD_COUNT):
                if board[i][j] == TAIL:
                    self.table[i][j] = OUT_REWARD
                elif board[i][j] == FOOD:
                    self.table[i][j] = FOOD_REWARD

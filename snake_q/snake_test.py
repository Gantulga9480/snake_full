from snake_game import Game
import numpy as np
import json
import time
from tkinter import Tk, filedialog
tk_root = Tk()
tk_root.withdraw()
dir_name = filedialog.askopenfilename()
data_file = open(dir_name, 'r')
q_table = json.load(data_file)
game = Game()
scores = 0
for i in range(100):
    state = game.reset()
    while not game.over:
        if state not in q_table:
            game.over = True
            print('state not ready')
        else:
            action = np.argmax(q_table[state])
            _, n_state, reward = game.step(action)
            state = n_state
    # time.sleep(5)
    scores += len(game.snake) - 3
    game.caption(f'{scores} : {scores/(i+1)}')
print(scores/100)

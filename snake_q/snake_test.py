from snake_game import Game
from tkinter import Tk, filedialog
import numpy as np
import json
tk_root = Tk()
tk_root.withdraw()
dir_name = filedialog.askopenfilename()
data_file = open(dir_name, 'r')
q_table = json.load(data_file)
game = Game()
scores = []
for _ in range(100):
    state = game.reset()
    while not game.over:
        if state not in q_table:
            game.over = True
        else:
            action = np.argmax(q_table[state])
            _, n_state, reward = game.step(action)
            state = n_state
    scores.append(len(game.snake) - 3)
    game.caption(f'{len(scores)} : {sum(scores)/len(scores)}')
print(sum(scores)/len(scores))

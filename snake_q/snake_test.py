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
while game.run:
    state = game.reset()
    while not game.over:
        if state not in q_table:
            game.over = True
        else:
            action = np.argmax(q_table[state])
            _, n_state, reward = game.step(action)
            state = n_state

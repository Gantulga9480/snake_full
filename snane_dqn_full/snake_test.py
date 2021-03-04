import os
import time
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model
from snake import Snake, FOOD_REWARD
from tkinter import Tk, filedialog
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
tk_root = Tk()
tk_root.withdraw()
dir_name = filedialog.askopenfilename()
main_nn = load_model(dir_name)
game = Snake(test=True)
scores = []
for _ in range(100):
    state = game.reset()
    counter = 0
    while not game.over:
        action_values = main_nn.predict(np.expand_dims(state, axis=0))[0]
        action = np.argmax(action_values)
        _, new_state, r = game.step(action=action)
        state = new_state
        counter += 1
        if counter > game.board_count * game.board_count * 10:
            game.over = True
        if r == FOOD_REWARD:
            counter = 0
    scores.append(len(game.snake) - 3)
    game.caption(f'{len(scores)} : {sum(scores)/len(scores)}')
print(sum(scores)/len(scores))

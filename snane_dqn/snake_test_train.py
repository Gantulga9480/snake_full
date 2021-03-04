from tensorflow import keras
from tensorflow.keras.models import load_model
from snake import *
import numpy as np
from matplotlib import pyplot as plt
import os
import random
from collections import deque
from tkinter import Tk, filedialog
tk_root = Tk()
tk_root.withdraw()
dir_name = filedialog.askopenfilename()
main_nn = load_model(dir_name)
name = "_".join(dir_name.split('/')[-1].split('_')[0:5])

# Hyperparameters
LEARNING_RATE = 0.001
DISCOUNT_RATE = 0.9
EPOCH = 1
BATCH_SIZE = 100
MAX_SCORE = 40
REPLAY_BUFFER = deque(maxlen=1000)
SAMPLES = []

# CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

game = Snake()
show_every = 5
episode = 1
history = {'reward': []}
ep_rewards = []
reward_tmp = 0
hour = 1
ep_index = 1


# Fit model
def keras_train():
    SAMPLES = random.sample(REPLAY_BUFFER, BATCH_SIZE)
    X = []
    Y = []
    for index, (state, action, _, reward, done, vals) in enumerate(SAMPLES):
        if not done:
            new_q = reward + DISCOUNT_RATE * np.max(vals)
        else:
            new_q = reward

        current_qs = vals
        current_qs[action] = new_q

        X.append(state)
        Y.append(current_qs)
    main_nn.fit(np.array(X), np.array(Y), epochs=EPOCH,
                shuffle=False, verbose=0)


while game.run:
    state = game.reset()
    ep_reward = 0
    score = 0
    action_counter = 0
    while not game.over:
        vals = main_nn.predict(np.expand_dims(state, axis=0))[0]
        action = np.argmax(vals)
        terminal, new_state, r = game.step(action=action)
        action_counter += 1
        ep_reward += r

        if r == FOOD_REWARD:
            score += 1
            action_counter = 0

        if action_counter > BOARD_COUNT**2:
            game.over = True
            terminal = True
            r = OUT_REWARD

        if terminal or r == FOOD_REWARD:
            REPLAY_BUFFER.append([state, action, new_state, r, terminal, vals])

        if len(REPLAY_BUFFER) >= BATCH_SIZE:
            keras_train()

        state = new_state

    ep_rewards.append(ep_reward)
    episode += 1

    if score > MAX_SCORE:
        MAX_SCORE = score
        info = f"{name}RE_sc{MAX_SCORE}_ep{episode}.h5"
        main_nn.save(info)

    if episode % show_every == 0:
        avg_r = sum(ep_rewards) / show_every
        ep_rewards.clear()
        if avg_r > reward_tmp:
            desc = f'avg: ↑ {avg_r} ep: {episode} '
        else:
            desc = f'avg: ↓ {avg_r} ep: {episode} '
        reward_tmp = avg_r
        history['reward'].append(avg_r)
        game.caption(desc)

info = f"{name}RE_sc{MAX_SCORE}_ep{episode}.h5"
main_nn.save(info)
main_nn.save(f"{name}RE.h5")
print("Training done congrat!!!")
plt.plot(history['reward'])
plt.show()

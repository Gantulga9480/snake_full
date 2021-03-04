from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Activation, Dense, Input, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import mixed_precision
from snake import *
import numpy as np
import random
from collections import deque
from matplotlib import pyplot as plt
from datetime import datetime as dt
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', default='')
args = parser.parse_args()

# Hyperparameters
LEARNING_RATE = 0.001
DISCOUNT_RATE = 0.5
EPSILON = 1
EPSILON_DECAY = .99999
MIN_EPSILON = 0.01
BATCH_SIZE = 256
EPOCH = 10
TARGET_NET_UPDATE_FREQUENCY = 5
UPDATE_COUNTER = 1
MAX_SCORE = 5

BUFFER_SIZE = 5000
MIN_BUFFER_SIZE = 1000
REPLAY_BUFFER = deque(maxlen=BUFFER_SIZE)
SAMPLES = []

INPUT_SHAPE = BOARD_COUNT * BOARD_COUNT
HIDDEN_LAYER_1 = INPUT_SHAPE * 2
HIDDEN_LAYER_2 = 8
OUT_SHAPE = len(ACTION_SPACE)
NETWORK = [INPUT_SHAPE, HIDDEN_LAYER_1, OUT_SHAPE]

# Mixed precision : RTX GPU only
# policy = mixed_precision.Policy('mixed_float16')
# mixed_precision.set_global_policy(policy)

# CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

game = Snake()
show_every = 5
episode = 1
history = {'ep': [], 'reward': []}
ep_rewards = []
reward_tmp = 0
hour = 1
ep_index = 1


# Test model in 1 game
def model_test(loop=False):
    game.caption('Test')
    test_reward = 0
    test_score = 0
    action_counter = 0
    while True:
        state = game.reset()
        while not game.over:
            action_values = main_nn.predict(np.expand_dims(state, axis=0))[0]
            action = np.argmax(action_values)
            _, new_state, r = game.step(action=action)
            state = new_state
            if not loop:
                test_reward += r
                if r == FOOD_REWARD:
                    test_score += 1
                    action_counter = 0
                if action_counter < BOARD_COUNT**2:
                    break
            action_counter += 1
        if not loop:
            print('test reward:', test_reward)
            print('test score:', test_score)
            print('------------------------')
            break
    return test_score


# Create new model with given specs
def get_model():
    model = Sequential()
    model.add(Input(shape=(INPUT_SHAPE,), name='input'))
    # model.add(Dense(HIDDEN_LAYER_1, activation='relu'))
    # model.add(Dense(HIDDEN_LAYER_2, activation='relu'))
    model.add(Dense(len(ACTION_SPACE)))
    # model.add(Activation('relu', dtype='float32'))  # TC enabled GPU only
    model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE),
                  metrics=["accuracy"])
    model.summary()
    return model


# Fit model
def keras_train():
    SAMPLES = random.sample(REPLAY_BUFFER, BATCH_SIZE)
    current_states = np.array([item[0] for item in SAMPLES])
    new_current_state = np.array([item[2] for item in SAMPLES])
    current_qs_list = []
    future_qs_list = []
    current_qs_list = main_nn.predict(current_states)
    future_qs_list = target_nn.predict(new_current_state)

    X = []
    Y = []
    for index, (state, action, _, reward, done) in enumerate(SAMPLES):
        if not done:
            new_q = reward + DISCOUNT_RATE * np.max(future_qs_list[index])
        else:
            new_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = new_q

        X.append(state)
        Y.append(current_qs)
    main_nn.fit(np.array(X), np.array(Y), epochs=EPOCH,
                batch_size=BATCH_SIZE, shuffle=False, verbose=0)


# Load model
try:
    main_nn = load_model(f"{args.index}.h5")
    target_nn = load_model(f"{args.index}.h5")
    print('LOADING MODEL')
except IOError:
    main_nn = get_model()
    target_nn = get_model()
    target_nn.set_weights(main_nn.get_weights())
    print('CREATING MODEL')


start_time = dt.now()
while game.run:
    state = game.reset()
    ep_reward = 0
    score = 0
    while not game.over:
        if np.random.random() < EPSILON:
            p_actions, _ = game.get_possible_actions()
            action = p_actions[np.random.randint(3)]
        else:
            action_values = main_nn.predict(np.expand_dims(state, axis=0))[0]
            action = np.argmax(action_values)
        terminal, new_state, r = game.step(action=action)
        REPLAY_BUFFER.append([state, action, new_state, r, terminal])
        EPSILON = EPSILON * EPSILON_DECAY
        ep_reward += r
        state = new_state

        if len(REPLAY_BUFFER) > MIN_BUFFER_SIZE:
            keras_train()
            UPDATE_COUNTER += 1

        if UPDATE_COUNTER % TARGET_NET_UPDATE_FREQUENCY == 0:
            target_nn.set_weights(main_nn.get_weights())
            UPDATE_COUNTER = 1

        if EPSILON < MIN_EPSILON:
            EPSILON = 0.1
            info = f"{args.index}_sc{MAX_SCORE}_ep{episode}_t{dtime[0]}.h5"
            main_nn.save(info)
            ep_index += 1

        if r == FOOD_REWARD:
            score += 1

        if game.save:
            time_now = dt.now()
            dtime = str(time_now - start_time).split(':')
            info = f"{args.index}_sc{MAX_SCORE}_ep{episode}_t{dtime[0]}.h5"
            main_nn.save(info)
            game.save = False

    ep_rewards.append(ep_reward)
    episode += 1

    if score > MAX_SCORE:
        MAX_SCORE = score
        time_now = dt.now()
        dtime = str(time_now - start_time).split(':')
        info = f"{args.index}_sc{MAX_SCORE}_ep{episode}_t{dtime[0]}.h5"
        main_nn.save(info)

    if episode % show_every == 0:
        time_now = dt.now()
        dtime = str(time_now - start_time).split(':')
        if int(dtime[0]) == hour:
            hour += 1
            scr = model_test()
        avg_r = sum(ep_rewards) / show_every
        ep_rewards.clear()
        if avg_r > reward_tmp:
            desc = f'avg: ↑ {avg_r} ep: {episode} eps: {EPSILON} '
        else:
            desc = f'avg: ↓ {avg_r} ep: {episode} eps: {EPSILON} '
        desc += f'{dtime[0]}:{dtime[1]}'
        reward_tmp = avg_r
        history['reward'].append(avg_r)
        history['ep'].append(EPSILON*100)
        game.caption(desc)

time_now = dt.now()
dtime = str(time_now - start_time).split(':')
info = f"{args.index}_sc{MAX_SCORE}_ep{episode}_t{dtime[0]}x{dtime[1]}.h5"
main_nn.save(info)
main_nn.save(f"{args.index}.h5")
print("Training done congrat!!!")
with open(f'{args.index}.txt', 'w+') as f:
    f.write(f'lr: {LEARNING_RATE}\n')
    f.write(f'gamma: {DISCOUNT_RATE}\n')
    f.write(f'batch size: {BATCH_SIZE}\n')
    f.write(f'buffer size {BUFFER_SIZE}\n')
    f.write(f'Network:\n')
    for item in NETWORK:
        f.write(f':  {item}\n')
plt.plot(history['reward'])
plt.plot(history['ep'])
plt.ylim([OUT_REWARD*1.2, FOOD_REWARD*50])
plt.show()

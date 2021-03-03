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

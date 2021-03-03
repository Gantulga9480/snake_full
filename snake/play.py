from snake import Snake

game = Snake(test=True)
while game.run:
    state = game.reset()
    while not game.over:
        game.step()

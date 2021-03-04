from snake import Snake

game = Snake()
while game.run:
    game.reset()
    while not game.over:
        game.step()

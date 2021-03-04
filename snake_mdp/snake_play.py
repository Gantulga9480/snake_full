import argparse
import snake as sg

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--description")
parser.add_argument("-c", "--colorful", action="store_true")
parser.add_argument("-sv", "--show_val", action="store_true")
parser.add_argument("-ur", "--update_rate", type=int)

args = parser.parse_args()

sg.init(args.description)
game = sg.Snake(colorful=args.colorful, num=args.show_val,
                update_rate=args.update_rate)
scores = []
for episode in range(100):
    state = game.reset()
    while not game.over:
        action = game.v.getAction(state)
        _, state, _ = game.step(action=action)
    scores.append(len(game.snake) - 3)
    # game.caption(f'{len(scores)} : {sum(scores)/len(scores)}')
print(sum(scores)/len(scores))

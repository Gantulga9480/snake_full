import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lenght', type=int)
args = parser.parse_args()


LEN = args.lenght
VEL = 20
SHAPE = VEL - 1
print(LEN)

clock = pygame.time.Clock()

while True:
    win = pygame.display.set_mode((VEL + VEL * (LEN + 2), VEL))
    win.fill((0, 0, 0))
    for i in range(LEN):
        if i == LEN - 1:
            pygame.draw.rect(win, (255, 255, 0), (VEL*i, 0, SHAPE, SHAPE))
        else:
            pygame.draw.rect(win, (255, 0, 0), (VEL*i, 0, SHAPE, SHAPE))
    pygame.draw.rect(win, (0, 255, 0), (VEL*(LEN + 2), 0, SHAPE, SHAPE))
    pygame.display.set_caption(f'{LEN} {VEL}')
    pygame.display.flip()
    clock.tick(60)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            quit()
        elif events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RIGHT:
                LEN += 1
            elif events.key == pygame.K_LEFT:
                LEN -= 1
            elif events.key == pygame.K_UP:
                VEL += 1
                SHAPE += 1
            elif events.key == pygame.K_DOWN:
                VEL -= 1
                SHAPE -= 1
            elif events.key == pygame.K_s:
                pygame.image.save(win, 'line.jpg')


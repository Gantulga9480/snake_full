import pygame
pygame.init()

VEL = 40
SHAPE = VEL - 1
win = pygame.display.set_mode((VEL*20 + 20, VEL*20 + 20))
font = pygame.font.SysFont("arial", 25)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    win.fill((0, 0, 0))
    pygame.draw.line(win, (255, 255, 255), (10, 10),
                     (VEL*20 + 10, 10))
    pygame.draw.line(win, (255, 255, 255), (10, 10),
                     (10, 10 + VEL*20))
    pygame.draw.line(win, (255, 255, 255), (VEL*20 + 10, 10),
                     (VEL*20 + 10, VEL*20 + 10))
    pygame.draw.line(win, (255, 255, 255), (10, VEL*20 + 10),
                     (VEL*20 + 10, VEL*20 + 10))
    # for i in range(10+1):
    #     pygame.draw.line(win, (255, 255, 255), (i*VEL + 10, 10),
    #                      (i*VEL + 10, 10*VEL + 10))
    #    pygame.draw.line(win, (255, 255, 255), (10, i*VEL + 10),
    #                      (10*VEL + 10, i*VEL + 10))
    pygame.draw.rect(win, (255, 255, 0), (VEL * 8 + 11, VEL * 8 + 11, SHAPE, SHAPE))
    pygame.draw.rect(win, (255, 0, 0), (VEL * 7 + 11, VEL * 8 + 11, SHAPE, SHAPE))
    pygame.draw.rect(win, (255, 0, 0), (VEL * 6 + 11, VEL * 8 + 11, SHAPE, SHAPE))
    pygame.draw.rect(win, (255, 0, 0), (VEL * 5 + 11, VEL * 8 + 11, SHAPE, SHAPE))

    pygame.draw.rect(win, (0, 255, 0), (VEL * 11 + 11, VEL * 10 + 11, SHAPE, SHAPE))

    pygame.draw.line(win, (255, 0, 255), (VEL * 11 + 11 +  + SHAPE//2, VEL * 8 + 11 +  + SHAPE//2),
                     (VEL * 11 + 11 +  + SHAPE//2, VEL * 10 + 11 +  + SHAPE//2), 5)

    pygame.draw.line(win, (0, 0, 255), (VEL * 8 + 11 + SHAPE//2, VEL * 8 + 11 + SHAPE//2),
                     (VEL * 11 + 11 +  + SHAPE//2, VEL * 8 + 11 +  + SHAPE//2), 5)

    # pygame.draw.rect(win, (0, 0, 255), (VEL * 3 + 11, VEL * 2 + 11, SHAPE, SHAPE))
    # pygame.draw.rect(win, (0, 0, 255), (VEL * 4 + 11, VEL * 3 + 11, SHAPE, SHAPE))
    # pygame.draw.rect(win, (0, 0, 255), (VEL * 3 + 11, VEL * 4 + 11, SHAPE, SHAPE))

    pygame.draw.line(win, (255, 255, 255), (VEL * 3 + 10, VEL*3 + 10),
                     (VEL*14 + 10, VEL*3 + 10))
    pygame.draw.line(win, (255, 255, 255), (VEL * 3 + 10, VEL*3 + 10),
                     (VEL*3 + 10, VEL*14 + 10))
    pygame.draw.line(win, (255, 255, 255), (VEL * 14 + 10, VEL*3 + 10),
                     (VEL*14 + 10, VEL*14 + 10))
    pygame.draw.line(win, (255, 255, 255), (VEL * 3 + 10, VEL*14 + 10),
                     (VEL*14 + 10, VEL*14 + 10))

    # for i in range(10):
    #     for j in range(10):
    #         state = font.render(f"{i},{j}", 1, (0, 0, 255))
    #         win.blit(state, (VEL * j + 17, VEL * i + 14))
    pygame.display.flip()

import pygame
import time
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

DIS_WIDTH = 800
DIS_HEIGHT = 600

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [DIS_WIDTH/2, DIS_HEIGHT/2])

def gameLoop():
    pygame.init()

    dis = pygame.display.set_mode((DIS_WIDTH, DIS_WIDTH))
    pygame.display.set_caption('Snake Game')

    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    snake_block = 10
    snake_speed = 30

    x1_change = 0
    y1_change = 0

    font_style = pygame.font.SysFont(None, 50)

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                if event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                if event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(WHITE)
        pygame.draw.rect(dis, BLUE, (0, 0, DIS_WIDTH - 1, DIS_HEIGHT - 1), 10)
        pygame.draw.rect(dis, BLACK, [x1, y1, snake_block, snake_block])
        pygame.display.update()

        clock.tick(snake_speed)

    message("You lost", RED)
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
    quit()


if __name__ == '__main__':
    gameLoop()
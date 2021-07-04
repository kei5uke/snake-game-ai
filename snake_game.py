import pygame
import random

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

DIS_WIDTH = 600
DIS_HEIGHT = 400

SNAKE_BLOCK = 10
SNAKE_SPEED = 15


class SnakeGame:
    def __init__(self):
        self.score = 0
        self.auto = False
        self.snake_observe = []
        self.loop = 0

    def generate_action(self):
        # 0 - up
        # 1 - right
        # 2 - down
        # 3 - left
        # key = random.randint(0, 3)
        return 1

    def start(self):
        pygame.init()
        self.gameLoop()

    def display_score(self, dis, score):
        score_font = pygame.font.SysFont("ornanong", 35)
        value = score_font.render("Your Score: " + str(score), True, YELLOW)
        dis.blit(value, [DIS_WIDTH / 3, 0])

    def display_message(self, dis, msg, color):
        font_style = pygame.font.SysFont("optima", 25)
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [DIS_WIDTH / 3, DIS_HEIGHT / 3])

    def plot_snake(self, dis, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, WHITE, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

    def gameLoop(self):
        pygame.display.set_caption('Snake Game')
        dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
        clock = pygame.time.Clock()

        game_over = False
        game_close = False

        x1 = DIS_WIDTH / 2
        y1 = DIS_HEIGHT / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

        while not game_over:

            while game_close == True:
                dis.fill(BLACK)
                self.display_message(dis, "DEAD! Press C:Play Again / Q:Quit", YELLOW)
                self.display_score(dis, Length_of_snake - 1)
                pygame.display.update()

                if not self.auto:
                    event = pygame.event.poll()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()

                if self.auto:
                    if self.loop == 0:
                        game_over = True
                        game_close = False
                    if self.loop > 0:
                        self.loop -= 1
                        self.gameLoop()

            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                game_over = True

            if self.auto:
                key = self.generate_action()
                if key == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif key == 1:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif key == 2:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
                elif key == 3:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0

            if not self.auto:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        y1_change = -SNAKE_BLOCK
                        x1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = SNAKE_BLOCK
                        y1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = SNAKE_BLOCK
                        x1_change = 0
                    elif event.key == pygame.K_LEFT:
                        x1_change = -SNAKE_BLOCK
                        y1_change = 0

            # End Flag: Snake goes outside of map
            if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
                game_close = True

            x1 += x1_change
            y1 += y1_change
            dis.fill(BLACK)
            pygame.draw.rect(dis, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            # End Flag: Snake eats his body
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            self.plot_snake(dis, snake_List)
            self.display_score(dis, Length_of_snake - 1)

            pygame.display.update()

            # Generate new food
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                Length_of_snake += 1

            clock.tick(SNAKE_SPEED)

        pygame.quit()
        quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.auto = True
    game.loop = 2
    game.start()

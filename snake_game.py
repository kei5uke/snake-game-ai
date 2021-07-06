import pygame
import random

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

SNAKE_BLOCK = 10
SNAKE_SPEED = 15


class SnakeGame:
    def __init__(self):
        self.dis_width = 600
        self.dis_height = 400
        self.display = pygame.display.set_mode((self.dis_width, self.dis_height))
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
        pygame.display.set_caption('Snake Game')
        self.gameLoop()
        return

    def display_message(self, mode, text):
        if mode == 'msg':
            font_style = pygame.font.SysFont("optima", 25)
            mesg = font_style.render(text, True, YELLOW)
            self.display.blit(mesg, [self.dis_width / 3, self.dis_height / 3])
        if mode == 'score':
            score_font = pygame.font.SysFont("ornanong", 35)
            value = score_font.render("Your Score: " + str(text), True, YELLOW)
            self.display.blit(value, [self.dis_width / 3, 0])

    def plot_snake(self, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.display, WHITE, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

    def plot_food(self, foodx, foody):
        pygame.draw.rect(self.display, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

    def generate_snake(self):
        x = round(random.randrange(0, self.dis_width - SNAKE_BLOCK) / 10.0) * 10.0
        y = round(random.randrange(0, self.dis_height - SNAKE_BLOCK) / 10.0) * 10.0
        return x, y

    def generate_food(self):
        foodx = round(random.randrange(0, self.dis_width - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, self.dis_height - SNAKE_BLOCK) / 10.0) * 10.0
        return foodx, foody

    def gameLoop(self):
        clock = pygame.time.Clock()

        game_over, game_close = False, False

        x1, y1 = self.generate_snake()
        x1_change, y1_change = 0, 0

        foodx, foody = self.generate_food()

        snake_List = []
        Length_of_snake = 1

        while not game_over:
            while game_close:
                # Game Close Menu
                self.display.fill(BLACK)
                self.display_message('msg', "DEAD! Press C:Play Again / Q:Quit")
                self.display_message('score', Length_of_snake - 1)
                self.score = Length_of_snake - 1
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
                    self.loop -= 1
                    if self.loop == 0:
                        game_over = True
                        game_close = False
                    if self.loop > 0:
                        self.gameLoop()

            # Get Key / Button Event
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                game_over = True

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

            # End Flag: Snake goes outside of map
            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                game_close = True

            self.display.fill(BLACK)

            x1 += x1_change
            y1 += y1_change

            # Update Snake
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

            self.plot_snake(snake_List)  # Plot Snake
            self.plot_food(foodx, foody)  # Plot Food
            self.display_message('score', Length_of_snake - 1)

            pygame.display.update()

            # Flag: Snake ate food
            if x1 == foodx and y1 == foody:
                foodx, foody = self.generate_food()  # Generate new food
                Length_of_snake += 1

            clock.tick(SNAKE_SPEED)
        pygame.quit()
        quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.auto = True
    game.loop = 2
    game.start()

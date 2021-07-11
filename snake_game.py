import pygame
import random
import numpy as np

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

SNAKE_BLOCK = 10
SNAKE_SPEED = 15


class snake_game:
    def __init__(self, width=600, height=400, auto=False, loop=0, step=0):
        self.dis_width = width
        self.dis_height = height
        self.display = pygame.display.set_mode((self.dis_width, self.dis_height))
        self.score = 0
        self.auto = auto
        self.snake_observe = []
        self.loop = loop
        self.step = step

    def start(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')

        if not self.auto:
            print('MANUAL GAME')
            self.gameLoop()

        if self.auto:
            for i in range(0, self.loop):
                print('AUTO GAME {0}'.format(i + 1))
                self.gameLoop()
        print('FINISHED')

    def generate_action(self):
        # 0 - up
        # 1 - right
        # 2 - down
        # 3 - left
        key = random.randint(0, 3)
        return key

    def get_key_action(self, event):
        key = None
        if self.auto:
            key = self.generate_action()
        elif not self.auto:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key = 0
                elif event.key == pygame.K_RIGHT:
                    key = 1
                elif event.key == pygame.K_DOWN:
                    key = 2
                elif event.key == pygame.K_LEFT:
                    key = 3
        return key

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

    def is_direction_blocked(self, x, y, snake_List):
        blocked_up, blocked_right, blocked_down, blocked_left = False, False, False, False
        if y - 10 == -10:
            blocked_up = True
        if x + 10 == self.dis_width:
            blocked_right = True
        if y + 10 == self.dis_height:
            blocked_down = True
        if x - 10 == -10:
            blocked_left = True
        for snake in snake_List[:-1]:
            if snake == [x, y - 10]:
                blocked_up = True
            if snake == [x + 10, y]:
                blocked_right = True
            if snake == [x, y + 10]:
                blocked_down = True
            if snake == [x - 10, y]:
                blocked_left = True

        return np.array([int(blocked_up), int(blocked_right), int(blocked_down), int(blocked_left)])

    def gameLoop(self):
        clock = pygame.time.Clock()
        game_over, game_close = False, False
        x1, y1 = self.generate_snake()
        x1_change, y1_change = 0, 0
        foodx, foody = self.generate_food()
        snake_List = []
        Length_of_snake = 1
        key = None
        action = None
        step = self.step

        blocked = self.is_direction_blocked(x1, y1, [[x1, y1]])

        while not game_over:
            if step == 0: return
            while game_close:
                if self.auto: return
                # Game Close Menu
                self.display.fill(BLACK)
                self.display_message('msg', "DEAD! Press C:Play Again / Q:Quit")
                self.display_message('score', Length_of_snake - 1)
                self.score = Length_of_snake - 1
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            return
                        elif event.key == pygame.K_c:
                            self.gameLoop()
                            return

            event = pygame.event.poll()
            # Quit Button Event
            if event.type == pygame.QUIT:
                game_over = True
            # Key Action Event
            key = self.get_key_action(event)
            if key == 0:  # up
                action = np.array([1, 0, 0, 0])
                y1_change = -SNAKE_BLOCK
                x1_change = 0
            elif key == 1:  # right
                action = np.array([0, 1, 0, 0])
                x1_change = SNAKE_BLOCK
                y1_change = 0
            elif key == 2:  # down
                action = np.array([0, 0, 1, 0])
                y1_change = SNAKE_BLOCK
                x1_change = 0
            elif key == 3:  # left
                action = np.array([0, 0, 0, 1])
                x1_change = -SNAKE_BLOCK
                y1_change = 0

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

            # End Flag: Snake goes outside of map
            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                game_close = True

            # End Flag: Snake eats his body
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            # Action Flag: Snake ate food
            if x1 == foodx and y1 == foody:
                foodx, foody = self.generate_food()  # Generate new food
                Length_of_snake += 1

            self.plot_snake(snake_List)  # Plot Snake
            self.plot_food(foodx, foody)  # Plot Food
            self.display_message('score', Length_of_snake - 1)

            if x1_change != 0 or y1_change != 0:
                # blocked : Blocked direction
                # action : Suggested action based on the blocked direction
                if game_close:
                    self.snake_observe.append([blocked, action, 1])
                    print([blocked, action, 1])
                elif not game_close:
                    self.snake_observe.append([blocked, action, 0])
                    print([blocked, action, 0])

                blocked = self.is_direction_blocked(x1, y1, snake_List)
                step -= 1

            clock.tick(SNAKE_SPEED)
            pygame.display.update()


if __name__ == "__main__":
    game = snake_game(auto=True, loop=2, step=10)
    game.start()
    print(game.score)
    print(game.snake_observe)
    print(game.step)
    print('blocked action')
    print(game.snake_observe)
    print(len(game.snake_observe))

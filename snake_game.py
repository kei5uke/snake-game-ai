import logging
import pygame
import random
import math
import sys
import numpy as np
from tensorflow.keras.models import load_model

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

SNAKE_BLOCK = 10
SNAKE_SPEED = 30
SNAKE_LENGTH = 3

logger = logging.getLogger(__name__)


class snake_game:
    def __init__(self, width=600, height=400):
        self.score = 0
        self.dis_width = width
        self.dis_height = height
        self.display = pygame.display.set_mode(
            (self.dis_width, self.dis_height))
        self.manual = False
        self.random = False
        self.auto = False
        self.loop = None
        self.step = None
        self.snake_observe = []
        self.model = None
        self.max = None

    def setting(self, mode, loop=1, step=None, model_file_name=None):
        self.manual, self.random, self.auto = False, False, False
        self.snake_observe = []  # Initialize
        if mode == 'manual':
            self.manual = True
        elif mode == 'random':
            self.random = True
        elif mode == 'auto':
            self.auto = True
            self.model = load_model(model_file_name)
        else:
            sys.exit('Select mode properly:' + mode)
        self.loop = loop
        self.step = step

    def start(self):
        '''Start snake game based on mode'''
        if self.manual == False and self.auto == False and self.random == False:
            sys.exit('Setting is missing')

        pygame.init()
        pygame.display.set_caption('Snake Game')

        if self.manual:
            logger.info('MANUAL GAME')
            self.gameLoop()

        elif self.random:
            for i in range(0, self.loop):
                logger.info('RANDOM GAME {0}'.format(i + 1))
                self.gameLoop()

        elif self.auto:
            for i in range(0, self.loop):
                logger.info('AUTO GAME {0}'.format(i + 1))
                self.gameLoop()

    def display_message(self, mode, text):
        ''' Display message '''
        if mode == 'msg':
            font_style = pygame.font.SysFont("optima", 30)
            mesg = font_style.render(text, True, YELLOW)
            self.display.blit(mesg, [0, 30])
        if mode == 'score':
            score_font = pygame.font.SysFont("ornanong", 30)
            value = score_font.render("Score: " + str(text), True, YELLOW)
            self.display.blit(value, [0, 0])

    def plot_snake(self, snake_list):
        ''' Plot snake on the map '''
        i = 0
        for x in list(reversed(snake_list)):
            if i % 2 == 0:
                pygame.draw.rect(self.display, GREEN, [
                                 x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])
            if i % 2 == 1:
                pygame.draw.rect(self.display, WHITE, [
                                 x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])
            i += 1

    def plot_food(self, foodx, foody):
        ''' Plot food on the map '''
        pygame.draw.rect(self.display, RED, [
                         foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

    def generate_snake(self):
        ''' Generate coordinate of snake '''
        x = round(random.randrange(
            0, self.dis_width - SNAKE_BLOCK) / 10.0) * 10.0
        y = round(random.randrange(
            0, self.dis_height - SNAKE_BLOCK) / 10.0) * 10.0
        return x, y

    def generate_food(self):
        ''' Generate coordinate of food '''
        foodx = round(random.randrange(
            0, self.dis_width - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(
            0, self.dis_height - SNAKE_BLOCK) / 10.0) * 10.0
        return foodx, foody

    def get_action_array(self, key):
        ''' One-hot encode of key action '''
        action = np.zeros(4)
        action[key] = 1
        return action

    def normalize_vector(self, vec):
        ''' Normalize vector in -1 ~ 1 '''
        return vec / np.linalg.norm(vec)

    def get_angle(self, x1, y1, x1_change, y1_change, foodx, foody):
        ''' Get andle of the direction of snake and food '''
        snake_dir = self.normalize_vector([x1_change, y1_change])
        food_dir = self.normalize_vector([(foodx - x1), (foody - y1)])
        angle = math.atan2(snake_dir[0] * food_dir[1] - snake_dir[1] * food_dir[0],
                           snake_dir[0] * food_dir[0] + snake_dir[1] * food_dir[1])
        return angle/math.pi

    def get_distance_of(self, x1, y1, x2, y2):
        ''' Get distance between snake and food '''
        return np.linalg.norm(np.array([(x2 - x1), (y2 - y1)]))

    def is_direction_blocked(self, x, y, snake_List):
        ''' Find blocked direction based on current location '''
        blocked_up, blocked_right, blocked_down, blocked_left = False, False, False, False
        if y - 10 == -10:
            blocked_up = True
        if x + 10 == self.dis_width:
            blocked_right = True
        if y + 10 == self.dis_height:
            blocked_down = True
        if x - 10 == -10:
            blocked_left = True
        for i in range(len(snake_List)):
            if i != (len(snake_List) - 2):
                if snake_List[i] == [x, y - 10]:
                    blocked_up = True
                if snake_List[i] == [x + 10, y]:
                    blocked_right = True
                if snake_List[i] == [x, y + 10]:
                    blocked_down = True
                if snake_List[i] == [x - 10, y]:
                    blocked_left = True

        return np.array([int(blocked_up), int(blocked_right), int(blocked_down), int(blocked_left)])

    def get_key_direction(self, key):
        ''' Get coordinate direction based on key '''
        x1_change, y1_change = 0, 0
        if key == 0:  # up
            y1_change = -SNAKE_BLOCK
            x1_change = 0
        elif key == 1:  # right
            x1_change = SNAKE_BLOCK
            y1_change = 0
        elif key == 2:  # down
            y1_change = SNAKE_BLOCK
            x1_change = 0
        elif key == 3:  # left
            x1_change = -SNAKE_BLOCK
            y1_change = 0

        return x1_change, y1_change

    def get_key_action(self, event, key):
        ''' Get key action from keyboard or random number '''
        if self.manual:
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

    def get_wall_distance(self, x1, y1):
        return np.array([self.get_distance_of(x1, y1, -SNAKE_BLOCK, y1)/self.dis_width+SNAKE_BLOCK,
                         self.get_distance_of(
                             x1, y1, self.dis_width, y1)/self.dis_width+SNAKE_BLOCK,
                         self.get_distance_of(
                             x1, y1, x1, -SNAKE_BLOCK)/self.dis_height+SNAKE_BLOCK,
                         self.get_distance_of(x1, y1, x1, self.dis_height)/self.dis_height+SNAKE_BLOCK])

    def get_auto_action(self, snake_List, foodx, foody, blocked):
        ''' Get predection based on given parameters
        Only used for auto game mode '''
        x1, y1 = snake_List[-1]
        key = 0
        prediction = []
        index = []
        for i in range(0, 4):
            action = self.get_action_array(i)
            x1_change, y1_change = self.get_key_direction(i)
            if (snake_List[-2][0] - snake_List[-1][0]) != x1_change or (snake_List[-2][1] - snake_List[-1][1]) != y1_change:
                angle = self.get_angle(
                    x1, y1, x1_change, y1_change, foodx, foody)
                X = x1 + x1_change
                Y = y1 + y1_change
                wall_distance = self.get_wall_distance(X, Y)
                food_distance = self.get_distance_of(
                    X, Y, foodx, foody) / self.max
                prediction.append(self.model.predict(np.hstack(
                    (blocked, action, angle, food_distance, wall_distance)).ravel().reshape(-1, 14)))
                index.append(i)
        key = index[np.argmax(prediction)]

        return key

    def gameLoop(self):
        ''' Main Game Function '''
        clock = pygame.time.Clock()
        game_over, game_close = False, False
        x1, y1 = self.generate_snake()
        x1_change, y1_change = 0, 0
        foodx, foody = self.generate_food()

        snake_Head = [x1, y1]
        if random.randint(0, 1) == 0:
            snake_List = [[x1 - 20, y1], [x1 - 10, y1], [x1, y1]]
        else:
            snake_List = [[x1, y1 - 20], [x1, y1 - 10], [x1, y1]]

        Length_of_snake = SNAKE_LENGTH
        key = random.randint(0, 3)
        action = None
        step = self.step
        blocked = self.is_direction_blocked(x1, y1, [[x1, y1]])
        distance = self.get_distance_of(x1, y1, foodx, foody)
        self.max = self.get_distance_of(
            0, 0, self.dis_width+SNAKE_BLOCK, self.dis_height+SNAKE_BLOCK)

        while not game_over:
            if step == 0:
                return
            while game_close:
                if self.random or self.auto:
                    return
                # Game Close Menu
                self.score = Length_of_snake - SNAKE_LENGTH
                self.display.fill(BLACK)
                self.display_message(
                    'msg', "DEAD! Press C:Play Again / Q:Quit")
                self.display_message('score', self.score)

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Quit game with Q
                            return
                        elif event.key == pygame.K_c:  # Continue with C
                            self.gameLoop()
                            return

            for event in pygame.event.get():
                # Quit Button Event
                if event.type == pygame.QUIT:
                    game_over = True
                # Key Action Event
                if self.manual == True:
                    key = self.get_key_action(event, key)

            if self.auto == True:
                key = self.get_auto_action(snake_List, foodx, foody, blocked)
            elif self.random == True:
                key = random.randint(0, 3)

            if key != None:
                new_x1_change, new_y1_change = self.get_key_direction(key)
                if (snake_List[-2][0] - snake_List[-1][0]) != new_x1_change or (snake_List[-2][1] - snake_List[-1][1]) != new_y1_change:
                    x1_change = new_x1_change
                    y1_change = new_y1_change
                    action = self.get_action_array(key)
                    angle = self.get_angle(
                        x1, y1, x1_change, y1_change, foodx, foody)

            # Update Snake
            if x1_change != 0 or y1_change != 0:
                x1 += x1_change
                y1 += y1_change
                snake_Head = []
                snake_Head.append(x1)
                snake_Head.append(y1)
                snake_List.append(snake_Head)
                if len(snake_List) > Length_of_snake:
                    del snake_List[0]

            # End Flag: Snake goes outside of map
            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                logger.info('DEAD: Went outside')
                game_close = True

            # End Flag: Snake eats his body
            for x in snake_List[:-1]:
                if x == snake_Head:
                    logger.info('DEAD: Eats himself')
                    game_close = True

            # Action Flag: Snake ate food
            if x1 == foodx and y1 == foody:
                logger.info('Score: Ate food')
                foodx, foody = self.generate_food()  # Generate new food
                Length_of_snake += 1

            self.display.fill(BLACK)
            self.plot_snake(snake_List)  # Plot Snake
            self.plot_food(foodx, foody)  # Plot Food
            self.display_message('score', Length_of_snake - SNAKE_LENGTH)

            # Collect data when snake moves
            if x1_change != 0 or y1_change != 0:
                new_distance = self.get_distance_of(x1, y1, foodx, foody)

                if self.score < Length_of_snake - SNAKE_LENGTH:
                    food_distance = 0
                else:
                    food_distance = new_distance / self.max
                wall_distance = self.get_wall_distance(x1, y1)
                data = np.hstack(
                    (blocked, action, angle, food_distance, wall_distance)).ravel()
                if game_close:
                    self.snake_observe.append([data, -1])
                    logger.debug('LABEL:-1')
                elif not game_close:
                    # Comparison of current location and previous location
                    if distance <= new_distance:
                        self.snake_observe.append([data, 0])
                        logger.debug('LABEL:0')
                    if distance > new_distance or self.score < Length_of_snake - SNAKE_LENGTH:
                        self.snake_observe.append([data, 1])
                        logger.debug('LABEL:1')
                logger.debug(f'BLOCKED:{blocked} ACTION:{action}')
                logger.debug(f'DEGREE:{math.degrees(angle*math.pi)}')
                logger.debug(f'WALL:{wall_distance}')
                logger.debug(f'FOOD:{food_distance}')

                # Update blocked direction, distance and score
                blocked = self.is_direction_blocked(x1, y1, snake_List)
                distance = new_distance
                self.score = Length_of_snake - SNAKE_LENGTH

                if step != None:
                    step -= 1
                    logger.debug(f'STEP:{step}')

            clock.tick(SNAKE_SPEED)
            pygame.display.update()


if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    module_levels = {__name__: logging.DEBUG}
    for module, level in module_levels.items():
        logging.getLogger(module).setLevel(level=level)

    game = snake_game()
    game.setting(mode='manual')
    game.start()
    game.setting(mode='random', loop=1, step=10)
    game.start()

from snake_game import snake_game

import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

import numpy as np

from logging import basicConfig, getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

class snake_nn:
    def __init__(self):
        self.model = None
        self.filename = './model/snake_nn_model.h5'

    def train(self, data):
        X, y = self.build_train_data(data)
        self.build_model()
        self.train_model(X, y)

    def build_train_data(self, data):
        X = np.array([i[0] for i in data]).reshape([-1, 9])
        y = np.array([i[1] for i in data]).reshape([-1, 1])
        logger.debug(X.shape)
        logger.debug(y.shape)
        return X, y

    def build_model(self):
        model = Sequential()
        model.add(Dense(10, activation='relu', input_dim=9))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['acc'])
        logger.debug(model.summary())
        self.model = model

    def train_model(self, X, y):
        self.model.fit(X,
                  y,
                  epochs = 16,
                  shuffle=True)
        self.model.save(self.filename)


if __name__ == "__main__":
    basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger.info('Start snake_nn.py')
    game = snake_game(auto=True, loop=500, step=100, model_file='./model/snake_nn_model.h5', width=100, height=100)
    game.start()
    snake_nn = snake_nn()
    snake_nn.train(game.snake_observe)
    logger.info('Finish snake_nn.py')

    new_game = snake_game(auto=True, model_file='./model/snake_nn_model.h5')
    new_game.start()

from snake_game import snake_game

import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

import numpy as np

from logging import basicConfig, getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

class snake_nn:
    def __init__(self, filename='./model/snake_nn_model.h5'):
        self.model = None
        self.filename = filename

    def train(self, data):
        ''' Start process of training
        1. Create training data
        2. Build_model
        3. Train nn model '''
        X, y = self.create_train_data(data)
        self.build_model()
        self.train_model(X, y)

    def create_train_data(self, data):
        ''' Divide data into x and y '''
        X = np.array([i[0] for i in data]).reshape([-1, 9])
        y = np.array([i[1] for i in data]).reshape([-1, 1])
        logger.debug(X.shape)
        logger.debug(y.shape)
        return X, y

    def build_model(self):
        ''' Build model '''
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
        ''' Train model '''
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
    game = snake_game(mode='auto', loop=100, step=10, model_file='./model/survive_and_apple/snake_nn_model_angle.h5', width=100, height=100)
    game.start()
    snake_nn = snake_nn()
    snake_nn.train(game.snake_observe)

    new_game = snake_game(mode='auto', model_file='./model/snake_nn_model.h5')
    new_game.start()

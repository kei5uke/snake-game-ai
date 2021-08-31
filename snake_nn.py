from snake_game import snake_game

import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import numpy as np

import logging
logger = logging.getLogger(__name__)


class snake_nn:
    def train(self, data, filename):
        ''' Start process of training
        1. Create training data
        2. Build_model
        3. Train nn model '''
        X, y = self.create_train_data(data)
        model = self.build_model()
        self.train_model(model, filename, X, y)

    def create_train_data(self, data):
        ''' Divide data into x and y '''
        X = np.array([i[0] for i in data]).reshape([-1, 9])
        y = np.array([i[1] for i in data]).reshape([-1, 1])
        logger.debug(f'Xshape:{X.shape} Yshape:{y.shape}')
        return X, y

    def build_model(self):
        ''' Build model '''
        model = Sequential()
        model.add(Dense(1, activation='relu', input_dim=9))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mean_squared_logarithmic_error',
                  optimizer='adam',
                  metrics=['acc'])
        logger.debug(model.summary())
        return model

    def train_model(self, model, filename, X, y):
        ''' Train model '''
        model.fit(X,
                  y,
                  epochs = 16,
                  shuffle=True,
                  batch_size = 16)
        model.save(filename)

if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    module_levels = {'snake_game':logging.DEBUG,__name__: logging.DEBUG}
    for module, level in module_levels.items():
        logging.getLogger(module).setLevel(level=level)

    game = snake_game()

    nn = snake_nn()
    gen = [1000, 2000, 5000, 100000]
    for g in gen:
        game.setting(mode = 'random', loop = g, step = 100)
        game.start()
        d = game.snake_observe
        name = 'gen' + str(g)
        nn = snake_nn()
        nn.train(d, name + '.h5')

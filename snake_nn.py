from snake_game import snake_game
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import regularizers
from tensorflow.keras import optimizers
import numpy as np

import logging
logger = logging.getLogger(__name__)

DIM = 14

class snake_nn:
    def __init__(self):
        self.history = None

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
        X = np.array([i[0] for i in data]).reshape([-1, DIM])
        y = np.array([i[1] for i in data]).reshape([-1, 1])
        logger.debug(f'Xshape:{X.shape}, Yshape:{y.shape}')
        return X, y

    def build_model(self):
        ''' Build model '''
        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=DIM))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='linear'))
        sgd = optimizers.Adam(lr=0.01)
        model.compile(loss='mean_squared_error',
                  optimizer=sgd,
                  metrics=['acc'])
        logger.debug(model.summary())
        return model

    def train_model(self, model, filename, X, y):
        ''' Train model '''
        self.history = model.fit(X,
                  y,
                  epochs = 4,
                  shuffle=True)
        model.save(filename)

if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    module_levels = {'snake_game':logging.INFO,__name__: logging.DEBUG}
    for module, level in module_levels.items():
        logging.getLogger(module).setLevel(level=level)

    game = snake_game()
    game.setting(mode = 'random', loop = 1000, step = 100)
    game.start()

    data = game.snake_observe
    nn = snake_nn()
    nn.train(data = data, model_file_name = 'test.h5')

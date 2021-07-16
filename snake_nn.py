from snake_game import snake_game

import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

import numpy as np

class snake_nn:
    def __init__(self):
        self.model = None
        self.filename = 'snake_nn_model.h5'

    def train(self, data):
        X, y = self.build_train_data(data)
        self.build_model()
        self.train_model(X, y)

    def build_train_data(self, data):
        X = np.array([i[0] for i in data]).reshape([-1, 8])
        y = np.array([i[1] for i in data]).reshape([-1, 1])
        print(X.shape)
        print(y.shape)
        return X, y

    def build_model(self):
        model = Sequential()
        model.add(Dense(10, activation='relu', input_dim=8))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])
        print(model.summary())
        self.model = model

    def train_model(self, X, y):
        self.model.fit(X,
                  y,
                  epochs = 16,
                  shuffle=True)
        self.model.save(self.filename)


if __name__ == "__main__":
    game = snake_game(random=True, loop=10, step=10)
    game.start()
    snake_nn = snake_nn()
    snake_nn.train(game.snake_observe)
    new_game = snake_game(auto=True, model_file='snake_nn_model.h5')
    new_game.start()

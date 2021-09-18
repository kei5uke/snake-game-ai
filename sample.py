from snake_game import snake_game

if __name__ == '__main__':
    game = snake_game()

    Play manual mode
    game.setting(mode = 'manual')
    game.start()

    # See auto-mated snake
    game.setting(mode = 'auto', model_file_name = './model/sample.h5')
    game.start()

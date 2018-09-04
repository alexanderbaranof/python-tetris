from tetris import *
import pygame
import random
import os
import json

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)


O = [[[1, 1],
      [1, 1]]]

I = [[[1, 1, 1, 1]],
     [[0, 1],
      [0, 1],
      [0, 1],
      [0, 1]]]

J = [[[1, 0, 0],
      [1, 1, 1]],
     [[0, 1],
      [0, 1],
      [1, 1]],
     [[1, 1, 1],
      [0, 0, 1]],
     [[1, 1],
      [1, 0],
      [1, 0]]]

L = [[[0, 0, 1],
      [1, 1, 1]],
     [[1, 1],
      [0, 1],
      [0, 1]],
     [[1, 1, 1],
      [1, 0, 0]],
     [[1, 0],
      [1, 0],
      [1, 1]]]

T = [[[0, 1, 0],
      [1, 1, 1]],
     [[0, 1],
      [1, 1],
      [0, 1]],
     [[1, 1, 1],
      [0, 1, 0]],
     [[1, 0],
      [1, 1],
      [1, 0]]]

S = [[[0, 1, 1],
      [1, 1, 0]],
     [[1, 0],
      [1, 1],
      [0, 1]]]

Z = [[[1, 1, 0],
      [0, 1, 1]],
     [[0, 1],
      [1, 1],
      [1, 0]]]

FORMS = [O, I, J, L, T, S, Z]


def load_config():
    assert os.path.exists('config.json')
    file = open('config.json', 'r')
    data = json.load(file)
    return data




def main(config_data):
    WIDTH = config_data['WIDTH']
    HEIGHT = config_data['HEIGHT']
    CELL_SIZE = config_data['CELL_SIZE']
    SPEED = config_data['SPEED']
    pygame.init()
    size = [CELL_SIZE * WIDTH, CELL_SIZE * HEIGHT]
    screen = pygame.display.set_mode(size)
    field = Field(WIDTH, HEIGHT)
    figure = Figure(field, screen, random.choice(FORMS), 0)
    pygame.time.set_timer(pygame.KEYDOWN, SPEED)
    pygame.display.set_caption("Tetris")
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.fill(BLACK)
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if figure.can_move_right(field):
                        figure.move_right(screen)
                elif event.key == pygame.K_LEFT:
                    if figure.can_move_left(field):
                        figure.move_left(screen)
                elif event.key == pygame.K_UP:
                    if figure.can_rotate(field):
                        figure.rotate(screen)
                elif event.key == pygame.K_SPACE:
                    pygame.time.set_timer(pygame.KEYDOWN, SPEED // 10)
                else:
                    if figure.can_move_down(field):
                        figure.move_down(screen)
                    else:
                        figure.to_map(field)
                        field.delete_rows()
                        field.draw(screen)
                        if not field.is_full():
                            pygame.time.set_timer(pygame.KEYDOWN, SPEED)
                            figure = Figure(field, screen, random.choice(FORMS), 0)
                        else:
                            done = True
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    config_data = load_config()
    main(config_data)
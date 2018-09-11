import pygame
import random
import os
import json

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)

assert os.path.exists('config.json')
file = open('config.json', 'r')
data = json.load(file)

WIDTH = data['WIDTH']
HEIGHT = data['HEIGHT']
EMPTY = 0
FULL = 1
CELL_SIZE = data['CELL_SIZE']
SPEED = data['SPEED']


class Field:
    '''The class describes the playing field'''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [([FULL] + [EMPTY] * self.width + [FULL])
                    for i in range(self.height)] + [[FULL] * (self.width + 2)]

    def draw(self, screen):
        screen.fill(BLACK)
        for y in range(self.height):
            for x in range(1, self.width + 1):
                if self.map[y][x] != EMPTY:
                    pygame.draw.rect(screen, self.map[y][x],
                                     [(x - 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE])

    def delete_rows(self):
        for y in range(self.height):
            if EMPTY not in self.map[y]:
                self.map = [[FULL] + [EMPTY] * self.width + [FULL]] + self.map[:y] + self.map[y + 1:]

    def is_full(self):
        return self.map[0][1:-1] != [0] * self.width


class Figure:
    '''The class describes any figure'''
    def __init__(self, field, screen, forms, turn):
        self.x = field.width // 2 - 1    #start point
        self.y = 0
        self.forms = forms
        self.turn = turn
        self.form = self.forms[self.turn]
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.draw(screen, self.color)

    def draw(self, screen, color=WHITE):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    pygame.draw.rect(screen, color,
                                     [(self.x + x) * CELL_SIZE, (self.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE])

    def can_move_down(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    if field.map[self.y + y + 1][self.x + x + 1] != EMPTY:
                        return False
        return True

    def can_move_right(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    if field.map[self.y + y][self.x + x + 2] != EMPTY:
                        return False
        return True

    def can_move_left(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    if field.map[self.y + y][self.x + x] != EMPTY:
                        return False
        return True

    def can_rotate(self, field):
        next_form = self.forms[(self.turn + 1) % len(self.forms)]
        for y in range(len(next_form)):
            for x in range(len(next_form[y])):
                if next_form[y][x] == FULL:
                    if field.map[self.y + y][self.x + x + 1] != EMPTY:
                        return False
        return True

    def move_down(self, screen):
        self.draw(screen, BLACK)
        self.y += 1
        self.draw(screen, self.color)

    def move_left(self, screen):
        self.draw(screen, BLACK)
        self.x -= 1
        self.draw(screen, self.color)

    def move_right(self, screen):
        self.draw(screen, BLACK)
        self.x += 1
        self.draw(screen, self.color)

    def rotate_form(self, forma):
	    return [ [ forma[y][x]
		    	for y in range(len(forma)) ]
                    for x in range(len(forma[0]) - 1, -1, -1) ]

    def rotate(self, field):
        self.draw(field, BLACK)
        self.form = self.rotate_form(self.form)
        self.draw(field, self.color)

    def to_map(self, field):
        for y in range(len(self.form)):
            for x in range(len(self.form[y])):
                if self.form[y][x] == FULL:
                    field.map[self.y + y][self.x + x + 1] = self.color
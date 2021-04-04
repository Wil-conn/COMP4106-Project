import grass_class
import fire_class
import dirt_class
import tree_class
import sheep_class
from settings import TILE_SIZE
from settings import GAME_SIZE
import settings
import numpy as np
import random
import math
import animal


class wolf(animal.animal):
    def __init__(self, x, y, colour, range, food, tile):
        super().__init__(x, y, colour, range, food, tile)
        '''
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "gray"
        self.range = 4
        self.movable = True
        self.food = 20
        self.tile_on = tile
        '''

    def cycle(self, environment, round):
        if self.food == 0:
            return self.starve()
        move_x = random.randrange(-1, 2, 1)
        move_y = random.randrange(-1, 2, 1)

        if self.x < TILE_SIZE:
            move_x += 1
        elif self.x >= GAME_SIZE-(TILE_SIZE+1):
            move_x -= 1
        if self.y < TILE_SIZE:
            move_y += 1
        elif self.y >= GAME_SIZE-(TILE_SIZE+1):
            move_y -= 1
        return self.move(self.x + (move_x * TILE_SIZE), self.y + (move_y * TILE_SIZE))
    '''
    def consume(self):
        if isinstance(self.tile_on, grass_class.grass):
            self.food += 1  # if the sheep consumes a grass tile, it gets 1 point of hunger back
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def starve(self):
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def move(self, x, y):
        self.x = x
        self.y = y
        m = (x, y, self)
        return m
    '''

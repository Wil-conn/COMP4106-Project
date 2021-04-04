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

    def cycle(self, environment, round):
        if self.food == 0:
            return self.starve()

        sheep_location = self.get_location_of_object(sheep_class.sheep, environment)

        if round == 0:
            move_x = random.randrange(-1, 2, 1)
            move_y = random.randrange(-1, 2, 1)

        else:
            if len(sheep_location) != 0:
                best_move = self.chooseMove(environment)
                #print("BEST MOVE IS : "+str(best_move))
                move_y = best_move[0]
                move_x = best_move[1]
            else:
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

    def chooseMove(self, environment):
        move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        grass_locations = self.get_location_of_object(grass_class.grass, environment)
        tree_location = self.get_location_of_object(tree_class.tree, environment)
        sheep_location = self.get_location_of_object(sheep_class.sheep, environment)
        wolf_location = self.get_location_of_object(wolf, environment)

        for element in sheep_location:
            up = abs(move[0][0] - element[0]) + abs(move[0][1] - element[1])
            down = abs(move[1][0] - element[0]) + abs(move[1][1] - element[1])
            left = abs(move[2][0] - element[0]) + abs(move[2][1] - element[1])
            right = abs(move[3][0] - element[0]) + abs(move[3][1] - element[1])

            l = [up, down, left, right]

            heur = (l.index(min(l)), (min(l)))

            try:
                if heur[1] < h1[1]:
                    h1 = heur
            except:
                h1 = heur

        return move[h1[0]]

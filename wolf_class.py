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
import game


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
        for rows in environment:
            for element in rows:
                if(element != None):
                    if self.x-1 <= element.x <= self.x+1 or self.y-1 <= element.y <= self.y+1:
                        if isinstance(element, fire_class.fire) and settings.WEATHER != "Rain":
                            return self.burn() #if sheep is adjacent to fire, 50% chance it burns
        return self.move(self.x + (move_x * TILE_SIZE), self.y + (move_y * TILE_SIZE))

    def chooseMove(self, environment):
        # wolves have the ability to move 8 direction instead of 4 like sheep
        move = [(-1, 0), (-1, -1), (-1, 1), (1, 0), (1, -1), (1, 1), (0, -1), (0, 1)]
        grass_locations = self.get_location_of_object(grass_class.grass, environment)
        tree_location = self.get_location_of_object(tree_class.tree, environment)
        fire_location = self.get_location_of_object(fire_class.fire, environment)
        sheep_location = self.get_location_of_object(sheep_class.sheep, environment)
        wolf_location = self.get_location_of_object(wolf, environment)

        if len(fire_location) > 0:
            print(fire_location)
            for element in fire_location:
                # because the wolves can move diagonally the Euclidian distance is a better heuristic
                l = self.move_calc(element, move)

                heur = (l.index(min(l)), (min(l)))

                try:
                    if heur[1] < h1[1]:
                        h1 = heur
                except:
                    h1 = heur
            opp = move[h1[0]]
            print('wolf')
            print(opp)
            opp = (opp[0]*-1, opp[1]*-1)
            print(opp)
            return opp
        else:
            for element in sheep_location:
                # because the wolves can move diagonally the Euclidian distance is a better heuristic
                l = self.move_calc(element, move)

                heur = (l.index(min(l)), (min(l)))

                try:
                    if heur[1] < h1[1]:
                        h1 = heur
                except:
                    h1 = heur

            return move[h1[0]]

    def move_calc(self, element, move):
        up = math.sqrt((move[0][0] - element[0])**2 + (move[0][1] - element[1])**2)
        up_left = math.sqrt((move[1][0] - element[0])**2 + (move[1][1] - element[1])**2)
        up_right = math.sqrt((move[2][0] - element[0])**2 + (move[2][1] - element[1])**2)
        down = math.sqrt((move[3][0] - element[0])**2 + (move[3][1] - element[1])**2)
        down_left = math.sqrt((move[4][0] - element[0])**2 + (move[4][1] - element[1])**2)
        down_right = math.sqrt((move[5][0] - element[0])**2 + (move[5][1] - element[1])**2)
        left = math.sqrt((move[6][0] - element[0])**2 + (move[6][1] - element[1])**2)
        right = math.sqrt((move[7][0] - element[0])**2 + (move[7][1] - element[1])**2)

        return [up, up_left, up_right, down, down_left, down_right, left, right]

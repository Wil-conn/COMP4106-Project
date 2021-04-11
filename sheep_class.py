import grass_class
import fire_class
import dirt_class
import tree_class
from settings import TILE_SIZE
from settings import GAME_SIZE
import settings
import time
import numpy as np
#from numpy import random
import random
import math
import animal


class sheep(animal.animal):
    def __init__(self, x, y, colour, range, food, tile):
        super().__init__(x, y, colour, range, food, tile)

    def cycle(self, environment, round):
        if self.food == 0:
            return self.starve()

        self.food -= 1

        # finds the location of any grass tiles in its view
        grass_locations = self.get_location_of_object(grass_class.grass, environment)

        # During cycle 0 the sheep gets a random move to make to initialize it
        if round == 0:
            move_x = random.randrange(-1, 2, 1)
            move_y = random.randrange(-1, 2, 1)

        # if there is a grass tile in it's view it will try to move towards it. otherwise it makes a random move
        '''
        else:
            if len(grass_locations) != 0:
                best_move = self.chooseMove(environment)
                #print("BEST MOVE IS : "+str(best_move))
                move_y = best_move[0]
                move_x = best_move[1]
            else:
                move_x = random.randrange(-1, 2, 1)
                move_y = random.randrange(-1, 2, 1)
'''
        best_move = self.chooseMove(environment)
        move_y = best_move[0]
        move_x = best_move[1]
        # checks to make sure it doesn't go off board
        if self.x < TILE_SIZE and move_x == -1:
            #print("INSIDE SELF.x < TILE SIZE IF ")
            move_x += 1
        elif self.x >= GAME_SIZE-(TILE_SIZE+1) and move_x == 1:
            #print("INSIDE SELF.x >= GAME_SIZE - (TILE_SIZE+1) IF ")
            move_x -= 1
        if self.y < TILE_SIZE and move_y == -1:
            #print("INSIDE SELF.y < TILE SIZE IF ")
            move_y += 1
        elif self.y >= GAME_SIZE-(TILE_SIZE+1) and move_y == 1:
            #print("INSIDE SELF.y >= GAME_SIZE - (TILE_SIZE+1) IF ")
            move_y -= 1

        #end random movement gen
        i, j = -(self.range), -(self.range)
        for rows in environment:
            for element in rows:
                #print(i, j)
                if(element != None):
                    if self.x-1 <= element.x <= self.x+1 or self.y-1 <= element.y <= self.y+1:
                        if isinstance(element, fire_class.fire) and settings.WEATHER != "Rain" and -1 <= j <= 1 and -1 <= i <= 1:
                            return self.burn() #if sheep is adjacent to fire, 50% chance it burns
                j += 1
            j = self.range * -1
            i += 1
        #input("Press Enter to continue...")
        return self.move(self.x + (move_x * TILE_SIZE), self.y + (move_y * TILE_SIZE))
        #return self.consume()

    # This is a very inelegant implementation but it works and that is all that matters
    # might clean it up later if we have time
    def chooseMove(self, environment):

        move = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # gets the locations of all the grass, tree, and sheep tiles the sheep can see in it's view
        grass_locations = self.get_location_of_object(grass_class.grass, environment)
        tree_location = self.get_location_of_object(tree_class.tree, environment)
        fire_location = self.get_location_of_object(fire_class.fire, environment)
        sheep_location = self.get_location_of_object(sheep, environment)
        #print(len(grass_locations))
        if(len(fire_location) > 0):
            for element in fire_location:
                # calculates the manhattan distance for each direction it can move
                up = abs(move[0][0] - element[0]) + abs(move[0][1] - element[1])
                down = abs(move[1][0] - element[0]) + abs(move[1][1] - element[1])
                left = abs(move[2][0] - element[0]) + abs(move[2][1] - element[1])
                right = abs(move[3][0] - element[0]) + abs(move[3][1] - element[1])

                l = [up, down, left, right]
                # l.index(min(l)) gets which move has the min value where 0 is up, 1 is down, 2 is left, 3 is right
                # also gets the values associated with that move and saves them in the tuple move
                heur = (l.index(min(l)), (min(l)))

                #makes sure doesn't move to tile sheep cant be on
                c = 0
                while move[heur[0]] in tree_location or move[heur[0]] in sheep_location:
                    l[l.index(min(l))] = 100
                    heur = (l.index(min(l)), (min(l)))

                    if c == 5:
                        return (0, 0)
                    c += 1

                # this is used to pick the best move if there are multiple possible fire tiles the sheep can go to
                try:
                    if heur[1] < h1[1]:
                        h1 = heur
                except:
                    h1 = heur

                #get the best move (going to the closest fire) and do the opposite
                m = move[0]
                if h1[0] == 0:
                    m = move[1]
                elif h1[0] == 2:
                    m = move[3]
                elif h1[0] == 3:
                    m = move[2]
                #print('sheep')
                #print(move[h1[0]])
                #print(m)
                opp = move[h1[0]]
                opp = (opp[0]*-1, opp[1]*-1)
                m = opp
                #print(m)
                return m

        else:
            if (len(grass_locations)) == 0:
                c = 0
                rand_move = (random.randrange(-1, 2, 1), random.randrange(-1, 2, 1))
                #print("RANDOM MOVE " + str(rand_move))
                while rand_move in tree_location or rand_move in sheep_location:
                    #print("RANDOM MOVE CONTAINS SHEEP OR TREE")
                    rand_move = (random.randrange(-1, 2, 1), random.randrange(-1, 2, 1))
                    if c == 5:
                        return (0, 0)
                    c += 1
                return rand_move


            for element in grass_locations:
                #print("ELEMENT IN GRASS LOCATION: " + str(element))
                # calculates the manhattan distance for each direction it can move
                up = abs(move[0][0] - element[0]) + abs(move[0][1] - element[1])
                down = abs(move[1][0] - element[0]) + abs(move[1][1] - element[1])
                left = abs(move[2][0] - element[0]) + abs(move[2][1] - element[1])
                right = abs(move[3][0] - element[0]) + abs(move[3][1] - element[1])

                # The Euclidian distance, used for testing

                l = [up, down, left, right]
                #print(l)

                # l.index(min(l)) gets which move has the min value where 0 is up, 1 is down, 2 is left, 3 is right
                # also gets the values associated with that move and saves them in the tuple move
                heur = (l.index(min(l)), (min(l)))
                #print(heur)
                # check if the best move has a tree. If it does it sets the heuristic value of that move to 100, or some arbitrarily large number
                # Because of the view the sheep has the manhattan distance will never be 100 so the sheep will never pick that move with a tree
                c = 0
                while move[heur[0]] in tree_location or move[heur[0]] in sheep_location:
                    #print("BEST MOVE AT" + str(move[heur[0]]) + " HAS TREE")
                    #print("L BEFORE REMOVING " + str(l))
                    l[l.index(min(l))] = 100
                    #print("L BEFORE CRASH")
                    #print(l)
                    #print("C BEFORE CRASH")
                    #print(c)
                    heur = (l.index(min(l)), (min(l)))
                    #print("NEXT BEST LOCATION AT " + str(move[heur[0]]))
                    if c == 5:
                        return (0, 0)
                    c += 1
                # if the best move contains a tile we cannot stand on then we chose the next best move

                #print("the best move direction is " + str(moves[0]) + " with a value of " + str(moves[1]))
                #print(l)
                # this is used to pick the best move if there are multiple possible grass tiles the sheep can go to
                try:
                    if heur[1] < h1[1]:
                        h1 = heur
                except:
                    h1 = heur

            return move[h1[0]]

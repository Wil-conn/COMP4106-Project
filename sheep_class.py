import grass_class
import fire_class
import dirt_class
from settings import TILE_SIZE
from settings import GAME_SIZE
import settings
import numpy as np
#from numpy import random
import random
import math

class sheep:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "white"
        self.range = 3
        self.movable = True
        self.food = 50
        self.tile_on = tile #used to store what the tile was before the sheep moved on to it

    def cycle(self, environment, round):
        # print("sheep is on " + str(self.tile_on))
        if self.food == 0:
            return self.starve()
        #temp nums used for random movement
        #if round % 3 != 0:
        #    return None

        #print("movex and movey from random")
        #print(move_x, move_y)
        self.food -= 1

        grass_locations = []
        #print(environment)
        print(environment)
        # finds the location of any grass tiles in its view
        cx, cy = -(self.range), -(self.range)
        for row in environment:
            for element in row:
                if isinstance(element, grass_class.grass):
                    grass_locations.append((cx, cy))
                cx += 1
            cx = -(self.range)
            cy += 1
        print(grass_locations)

        #print("GRASS LOCATIONS: "+str(grass_locations))
        #print(grass_locations)
        if round == 0:
            move_x = random.randrange(-1, 2, 1)
            move_y = random.randrange(-1, 2, 1)

        else:
            if len(grass_locations) != 0:
                best_move = self.chooseMove(grass_locations)
                print("BEST MOVE IS : "+str(best_move))
                if best_move == "up":
                    move_x = 0
                    move_y = -1
                if best_move == "down":
                    move_x = 0
                    move_y = 1
                if best_move == "left":
                    move_x = -1
                    move_y = 0
                if best_move == "right":
                    move_x = 1
                    move_y = 0
            else:
                move_x = 0
                move_y = 0
        if self.x <= TILE_SIZE:
            move_x += 1
        elif self.x >= GAME_SIZE-(TILE_SIZE+1):
            move_x -= 1
        if self.y <= TILE_SIZE:
            move_y += 1
        elif self.y >= GAME_SIZE-(TILE_SIZE+1):
            move_y -= 1
        #end random movement gen
        print("move_x = " + str(move_x) + " move_y = " + str(move_y))
        for rows in environment:
            for element in rows:
                if(element != None):
                    if self.x-1 <= element.x <= self.x+1 or self.y-1 <= element.y <= self.y+1:
                        if isinstance(element, fire_class.fire) and settings.WEATHER != "Rain":
                            return self.burn() #if sheep is adjacent to fire, 50% chance it burns
        #print("sheep class move_x move_y " + str(move_x) +","+str(move_y))
        #print("sheep class self.x self.y " + str(self.x) +","+str(self.y))
        #input("Press Enter to continue...")
        return self.move(self.x + (move_x * TILE_SIZE), self.y + (move_y * TILE_SIZE))
        #return self.consume()

    # This is a very inelegant implementation but it works and that is all that matters
    # might clean it up later if we have time
    def chooseMove(self, grass_locations):
        move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        '''
        moves = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        '''
        #print("NEW SHEEP")
        for element in grass_locations:
            print("ELEMENT IN GRASS LOCATION: " + str(element))
            # calculates the manhattan distance for each direction it can move
            up = abs(move[0][0] - element[0]) + abs(move[0][1] - element[1])
            down = abs(move[1][0] - element[0]) + abs(move[1][1] - element[1])
            left = abs(move[2][0] - element[0]) + abs(move[2][1] - element[1])
            right = abs(move[3][0] - element[0]) + abs(move[3][1] - element[1])
            '''
            up = math.sqrt((move[0][0]-element[1])**2 + (move[0][1] - element[1])**2)
            down = math.sqrt((move[1][0]-element[0])**2 + (move[1][1] - element[1])**2)
            left = math.sqrt((move[2][0]-element[0])**2 + (move[2][1] - element[1])**2)
            right = math.sqrt((move[3][0]-element[0])**2 + (move[3][1] - element[1])**2)
            '''

            l = (up, down, left, right)
            #print(l)

            # l.index(min(l)) gets which move has the min value where 0 is up, 1 is down, 2 is left, 3 is right
            # also gets the values associated with that move and saves them in the tuple move

            moves = (l.index(min(l)), (min(l)))
            #print("the best move direction is " + str(moves[0]) + " with a value of " + str(moves[1]))
            #print(l)
            try:
                if moves[1] < h1[1]:
                    h1 = moves
            except:
                h1 = moves
        print("PRNTING H1" + str(h1))
        #return moves[0]
        if h1[0] == 0:
            return "up"
        if h1[0] == 1:
            return "down"
        if h1[0] == 2:
            return "left"
        if h1[0] == 3:
            return "right"

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

    def consume(self):
        #print('consume')
        if isinstance(self.tile_on, grass_class.grass):
            self.food += 1 # if the sheep consumes a grass tile, it gets 1 point of hunger back
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def starve(self):
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def move(self, x, y):
        #m = (x, y, sheep(x, y))
        self.x = x
        self.y = y
        m = (x, y, self) #using self rather than creating a new sheep object lets us keep track of the sheeps hunger as they move around. creating a new sheep object just creates the illusion of move, sending self lets the actual object move around
        return m


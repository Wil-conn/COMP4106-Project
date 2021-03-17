import grass_class
import fire_class
import dirt_class
from settings import *
from numpy import random
import random

class sheep:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "white"
        self.range = 3
        self.movable = True
        self.food = 5
        self.name = name #used for testing. will probably be removed in the final version

    def cycle(self, environment, round): #round argument just for testing something. will be removed later
        print("sheep #"+str(self.name)+"has a hunger value of: "+str(self.food))
        #temp nums used for random movement
        move_x = random.randrange(-1, 2, 1)
        move_y = random.randrange(-1, 2, 1)
        self.food -= 1

        if self.x <= TILE_SIZE:
            move_x += 1
        elif self.x >= GAME_SIZE-(TILE_SIZE+1):
            move_x -= 1
        if self.y <= TILE_SIZE:
            move_y += 1
        elif self.y >= GAME_SIZE-(TILE_SIZE+1):
            move_y -= 1
        #end random movement gen

        for rows in environment:
            for element in rows:
                if(element != None):
                    if self.x-1 <= element.x <= self.x+1 or self.y-1 <= element.y <= self.y+1:
                        if isinstance(element, fire_class.fire):
                            return self.burn() #if sheep is adjacent to fire, 50% chance it burns
        print("sheep class move_x move_y " + str(move_x) +","+str(move_y))
        print("sheep class self.x self.y " + str(self.x) +","+str(self.y))
        return self.move(self.x + (move_x * TILE_SIZE), self.y + (move_y * TILE_SIZE))
        #return self.consume()

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

    def consume(self):
        #print('consume')
        self.food += 1
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def move(self, x, y):
        #print('move')
        #m = (x, y, sheep(x, y))
        self.x = x
        self.y = y
        m = (x, y, self) #using self rather than creating a new sheep object lets us keep track of the sheeps hunger as they move around. creating a new sheep object just creates the illusion of move, sending self lets the actual object move around
        return m


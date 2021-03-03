#from grass_class import grass
from grass_class import *
from numpy import random

class dirt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "brown"
        self.range = 1

    #determines what said block should do given its environment (i.e the blocks around it that it can observe given its range)
    #for the dirt block it goes through every element of its environment, if there is a grass block in its environment then there is a 20% chance said dirt block will become a grass block
    def cycle(self, environment):
        x = random.rand() * 100
        multiplyer = 1
        c = 0
        for rows in environment:
            for element in rows:
                if isinstance(element, grass):
                    c += 1
                    if c == 4:
                        return self.turn_to_grass()
                    elif x < 2:
                        return self.turn_to_grass()
        if x < 0.02:
            return self.turn_to_grass()
        c = 0
    #creates a new grass object and returns to the gameboard where this new object should be places
    def turn_to_grass(self):
        new_grass = grass(self.x, self.y)
        x = (self.x, self.y, grass(self.x, self.y))
        return x

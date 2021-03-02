from grass_class import grass
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
        for rows in environment:
            for element in rows:
                if isinstance(element, grass):
                    if x < 20:
                        return self.turn_to_grass()
        if x < 0.1:
            return self.turn_to_grass()
    #creates a new grass object and returns to the gameboard where this new object should be places
    def turn_to_grass(self):
        new_grass = grass(self.x, self.y)
        x = (self.x, self.y, new_grass)
        return x

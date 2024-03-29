#from grass_class import grass
import grass_class
import sheep_class
from settings import SHEEP_FOOD, SHEEP_RANGE, SHEEP_COLOUR
import settings
from numpy import random


class dirt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "brown"
        self.range = 1
        self.movable = False

    #determines what said block should do given its environment (i.e the blocks around it that it can observe given its range)
    #for the dirt block it goes through every element of its environment, if there is a grass block in its environment then there is a 20% chance said dirt block will become a grass block
    def cycle(self, environment, round):
        #m = 1 + (round / 300)
        #if round % 2 != 0: #this makes it grass only grows every 5 cycles
        #    return None

        x = random.rand() * 100
        grass_total = 0
        sheep_total = 0
        #print("m = " + str(m))

        for rows in environment:
            for element in rows:
                if isinstance(element, grass_class.grass):
                    grass_total += 1
                    #if c == 4:
                    #    return self.turn_to_grass()
                    #elif x * m < 2:
                    #    return self.turn_to_grass()
                if isinstance(element, sheep_class.sheep):
                    sheep_total += 1

        if sheep_total == 2:
            #print("SHEEP TOTAL:")
            #print(sheep_total)
            if x < 20:
                #print("REPRODUCING")
                return self.spawn_sheep()
        rain_bonus = 0
        if settings.WEATHER == "Rain":
            rain_bonus = 0.5
            if grass_total > 3:
                return self.turn_to_grass()
        if settings.WEATHER == "Sunny":
            if grass_total > 5:
                return self.turn_to_grass()

        if grass_total > 3:
            return self.turn_to_grass()

        #if 24.5 < x and x < 25+rain_bonus:
        if x < 0.3+rain_bonus:
            return self.turn_to_grass()
        c = 0
    #creates a new grass object and returns to the gameboard where this new object should be places
    def turn_to_grass(self):
        x = (self.x, self.y, grass_class.grass(self.x, self.y))
        return x

    def spawn_sheep(self):
        x = (self.x, self.y, sheep_class.sheep(self.x, self.y, SHEEP_COLOUR, SHEEP_RANGE, 4, dirt))
        return x


from numpy import *
'''
from tree_class import tree
from fire_class import fire
'''
import dirt_class
import fire_class
import tree_class
import sheep_class
import settings

class grass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "green"
        self.range = 1
        self.movable = False

    def cycle(self, environment, round):
        x = random.rand() * 100
        c = 0
        g = 0
        sheep_counter = 0
        if x < 0.01 and settings.WEATHER != "Rain":
            return self.burn() #there is a 0.05% chance a grass tile will self immulate, this is just for testing fire
        test = where(isinstance(environment.flat[0], dirt_class.dirt)) #ignore, was testing things
        for rows in environment:
            for element in rows:
                if isinstance(element, fire_class.fire) and settings.WEATHER != "Rain":
                    if x < 20:
                        return self.burn() #if there is fire next to a grass tile, there is a 20% chance the grass tile will catch on fire
                if isinstance(element, tree_class.tree):
                    c += 1
                    weather_bonus = 0
                    if settings.WEATHER == 'Sunny':
                        weather_bonus = 5
                    elif settings.WEATHER == 'Cloudy':
                        weather_bonus = -19
                    if c == 5:
                        if x < 20+weather_bonus:
                            return self.turn_to_tree()
                    if c == 7:
                        if x < 70+weather_bonus:
                            return self.turn_to_tree()
                if isinstance(element, sheep_class.sheep):
                    sheep_counter += 1
                '''
                if isinstance(element, grass):
                    #g += 1
                    if x < 3:
                        return self.spawn_sheep()  #sheep_number argument is just for testing something
                        '''
        if sheep_counter == 2:
            self.spawn_sheep()
        if x < 1 and settings.WEATHER != 'Cloudy': #0.1% chance any grass tile might turn into a tree
            return self.turn_to_tree()

    def turn_to_tree(self):
        #print("test")
        #pass
        x = (self.x, self.y, tree_class.tree(self.x, self.y))
        return x

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

    def spawn_sheep(self):
        #x = (self.x, self.y, sheep_class.sheep(self.x, self.y, grass)) #round argument just for testing, will be removed
        x = (self.x, self.y, sheep_class.sheep(self.x, self.y, settings.SHEEP_COLOUR, settings.SHEEP_RANGE, 4, dirt_class.dirt))
        return x

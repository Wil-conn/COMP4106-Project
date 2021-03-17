from numpy import *
'''
from tree_class import tree
from fire_class import fire
'''
import dirt_class
import fire_class
import tree_class
import sheep_class

sheep_number = 0

class grass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "green"
        self.range = 1
        self.movable = False

    def cycle(self, environment, round):
        global sheep_number
        x = random.rand() * 100
        c = 0
        g = 0
        if x < 0.01:
            return self.burn() #there is a 0.05% chance a grass tile will self immulate, this is just for testing fire
        test = where(isinstance(environment.flat[0], dirt_class.dirt)) #ignore, was testing things
        for rows in environment:
            for element in rows:
                if isinstance(element, fire_class.fire):
                    if x < 20:
                        return self.burn() #if there is fire next to a grass tile, there is a 20% chance the grass tile will catch on fire
                if isinstance(element, tree_class.tree):
                    c += 1
                    if c == 5:
                        if x < 40:
                            return self.turn_to_tree()
                    if c == 7:
                        return self.turn_to_tree()
                if isinstance(element, grass):
                    #g += 1
                    if x < 10:
                        sheep_number+=1
                        return self.spawn_sheep(sheep_number)  #round argument is just for testing something
        if x < 0.3: #0.1% chance any grass tile might turn into a tree
            return self.turn_to_tree()

    def turn_to_tree(self):
        x = (self.x, self.y, tree_class.tree(self.x, self.y))
        return x

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

    def spawn_sheep(self, round):
        x = (self.x, self.y, sheep_class.sheep(self.x, self.y, round))
        return x

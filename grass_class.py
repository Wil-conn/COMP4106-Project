from numpy import random
'''
from tree_class import tree
from fire_class import fire
'''
import tree_class
import fire_class

class grass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "green"
        self.range = 1

    def cycle(self, environment):
        x = random.rand() * 100
        c = 0
        if x < 0.01:
            return self.burn()
        for rows in environment:
            for element in rows:
                if isinstance(element, fire_class.fire):
                    if x < 30:
                        return self.burn()
                if isinstance(element, grass):
                    c += 1
                    if c == 6:
                        if x < 0.2:
                            return self.turn_to_tree()
                    if c == 11:
                        return self.turn_to_tree()
        if x < 0.01:
            return self.turn_to_tree()

    def turn_to_tree(self):
        x = (self.x, self.y, tree_class.tree(self.x, self.y))
        return x

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

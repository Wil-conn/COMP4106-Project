import fire_class
from numpy import random
class tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "dark green"
        self.range = 1

    def cycle(self, environment, round):
        for rows in environment:
            for element in rows:
                if isinstance(element, fire_class.fire):
                    return self.burn() #if there is a fire next to a tree that tree will always catch on fire
        return None

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

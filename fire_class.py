from numpy import random
#from dirt_class import dirt
import dirt_class
class fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "red"
        self.range = 1

    def cycle(self, environment):
        x = random.rand() * 100
        if x < 70:
            return self.extinguish()

    def extinguish(self):
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x


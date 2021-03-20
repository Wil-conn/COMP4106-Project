from numpy import random
import settings
#from dirt_class import dirt
class fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "red"
        self.range = 1
        self.movable = False

    def cycle(self, environment, round):
        x = random.rand() * 100
        if settings.WEATHER == "Rain":
            print("rain")
            return self.extinguish()
        if x < 80:
            return self.extinguish()

    def extinguish(self):
        import dirt_class
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x


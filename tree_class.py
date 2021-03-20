import fire_class
import random
import settings
class tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "dark green"
        self.range = 1
        self.movable = False

    def cycle(self, environment, round):
        for rows in environment:
            for element in rows:
                if isinstance(element, fire_class.fire) and settings.WEATHER != "Rain":
                    if random.randint(0,100) < 75:
                        return self.burn() #if there is a fire next to a tree there is a 75% chance it catches on fire
        if settings.WEATHER == "Lightning":
            if random.randint(0,100) < 10:
                return self.burn()# if the weather is lightning then there is a 10% chance a tree will get struck and catch fire
        return None

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        #print('burn')
        return x

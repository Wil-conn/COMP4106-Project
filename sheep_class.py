import grass_class
import fire_class
import dirt_class
import settings
from numpy import random
import random

class sheep:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = "white"
        self.range = 3
        self.movable = True

    def cycle(self, environment, round):
        print('help')
        #temp nums used for random movement
        move_x = random.randrange(-1, 2, 1)
        move_y = random.randrange(-1, 2, 1)
        
        if self.x <= 5:
            move_x += 1
        elif self.x >= settings.GAME_SIZE-6:
            move_x -= 1
        if self.y <= 5:
            move_y += 1
        elif self.y >= settings.GAME_SIZE-6:
            move_y -= 1
        #end random movement gen
        
        for rows in environment:
            for element in rows:
                if(element != None):
                    if self.x-1 <= element.x <= self.x+1 or self.y-1 <= element.y <= self.y+1:
                        if isinstance(element, fire_class.fire):
                            return self.burn() #if sheep is adjacent to fire, 50% chance it burns
        
        return self.move(self.x + (move_x * 5), self.y + (move_y * 5))
        #return self.consume()
    
    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

    def consume(self):
        print('consume')
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def move(self, x, y):
        print('move')
        m = (x, y, sheep(x, y))
        return m  
                
    

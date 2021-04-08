import grass_class
import fire_class
import dirt_class
import tree_class

class animal:
    def __init__(self, x, y, colour, range, food, tile):
        self.x = x
        self.y = y
        self.alive = True
        self.colour = colour
        self.range = range
        self.movable = True
        self.food = food
        self.tile_on = tile

    def get_location_of_object(self, object, environment):
        locations = []
        cx, cy = -(self.range), -(self.range)
        for row in environment:
            for element in row:
                if isinstance(element, object):
                    locations.append((cx, cy))
                cx += 1
            cx = -(self.range)
            cy += 1
        return locations

    def burn(self):
        x = (self.x, self.y, fire_class.fire(self.x, self.y))
        return x

    def consume(self):
        if isinstance(self.tile_on, grass_class.grass):
            self.food += 2 # if the sheep consumes a grass tile, it gets 1 point of hunger back
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def starve(self):
        print("STARVING")
        x = (self.x, self.y, dirt_class.dirt(self.x, self.y))
        return x

    def move(self, x, y):
        self.x = x
        self.y = y
        m = (x, y, self)
        return m


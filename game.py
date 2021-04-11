import tkinter
import numpy as np
import time
from settings import GAME_SIZE
from settings import TILE_SIZE
import settings
from dirt_class import dirt
from sheep_class import sheep
from grass_class import grass
from wolf_class import wolf
from tree_class import tree
from fire_class import fire
import random


class gameboard():
    def __init__(self, x, y, c):
        self.cols = x
        self.rows = y
        self.map = np.empty((self.cols, self.rows), dtype = object)
        self.c = c
        self.weather_cycle = 10
        self.sheep_statistics = []
        self.wolf_statistics = []
        self.grass_statistics = []
        self.tree_statistics = []
        self.fire_statistics = []

    #goes through every block in the array and draws it on screen according to its colour. every block has a size of 5x5 pixels
    def display(self):
        for i in range (0, self.rows, TILE_SIZE):
            for j in range (0, self.cols, TILE_SIZE):
                self.c.create_rectangle(i, j, i+TILE_SIZE, j+TILE_SIZE, fill = self.map[i][j].colour)
        self.c.create_rectangle(0, GAME_SIZE, GAME_SIZE, GAME_SIZE+50, fill="Grey")
        self.weather_id = self.c.create_text(GAME_SIZE/2, GAME_SIZE+10, fill="Black", text=settings.WEATHER)

    def update_block(self, x, y):
        #print(self.map[x][y])
        self.c.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill = self.map[x][y].colour)

    #adds a cell to the board. right now it only adds dirt
    def add_cell(self, x, y):
        r = random.randint(0,100)
        if r<=1:
            self.map[x][y] = sheep(x, y, "white", 3, 50, dirt)
        elif 1<r<=2:
            self.map[x][y] = wolf(x, y, "gray", 4, 20, dirt)
        elif 2 < r < 20:
            self.map[x][y] = grass(x, y)
        else:
            self.map[x][y] = dirt(x, y)

    #fills the board with dirt. used for when game is being initialize
    def fill_board(self):
        #print("test")
        for i in range (0, self.rows, TILE_SIZE):
            for j in range (0, self.cols, TILE_SIZE):
                self.add_cell(i, j)
        #self.map[13 * TILE_SIZE][13 * TILE_SIZE] = sheep(13 * TILE_SIZE, 13 * TILE_SIZE, "white", 5, 20, dirt)
        #self.map[10 * TILE_SIZE][10 * TILE_SIZE] = wolf(10 * TILE_SIZE, 10 * TILE_SIZE, "gray", 4, 20, dirt)
        #self.map[20 * TILE_SIZE][20 * TILE_SIZE] = wolf(20 * TILE_SIZE, 20 * TILE_SIZE, "gray", 4, 20, dirt)

    def update_weather(self):
        if self.weather_cycle == 0:
            r = random.randint(0,100)
            if r <= 25:
                settings.WEATHER = "Rain"
                self.weather_cycle = random.randrange(25, 30, 1)
            elif r > 25 and r <= 50:
                settings.WEATHER = "Sunny"
                self.weather_cycle = random.randrange(20, 40, 1)
            elif r > 50 and r <= 75:
                settings.WEATHER = "Cloudy"
                self.weather_cycle = random.randrange(20, 40, 1)
            else:
                settings.WEATHER = "Lightning"
                self.weather_cycle = random.randrange(10, 15, 1)
            self.c.delete(self.weather_id)
            self.weather_id = self.c.create_text(GAME_SIZE/2, GAME_SIZE+10, fill="Black", text=settings.WEATHER)

        else:
            self.weather_cycle -= 1

    #this returns an NxN array which contains all the objects in a radius R around a given block
    #this is used for determining what said block is able to "see"
    #ex: a dirt block only has knowledge of the blocks 1 block away from it, so it has an R of 1 and will return a 3x3 array of objects around it
    def radius_around_coord(self, x, y, r):
        view = np.empty(((r*2)+1, (r*2)+1), dtype = object)
        rows, cols = 0, 0

        for i in range (-(r*TILE_SIZE), (r*TILE_SIZE+1), TILE_SIZE):
            for j in range (-(r*TILE_SIZE), (r*TILE_SIZE+1), TILE_SIZE):
                if (x + i >= 0 and y + j >= 0) and (x + i < self.rows and y + j < self.cols):
                    view[rows][cols] = self.map[x+i][y+j]
                    cols += 1
                else:
                    view[rows][cols] = None
                    cols += 1
            rows += 1
            cols = 0
        return view

    def stats(self):
        num_sheep = 0
        num_wolf = 0
        num_grass = 0
        num_tree = 0
        num_fire = 0
        for i in range (0, self.rows, TILE_SIZE):
            for j in range (0, self.cols, TILE_SIZE):
                if isinstance(self.map[i][j], sheep):
                    num_sheep += 1
                if isinstance(self.map[i][j], wolf):
                    num_wolf += 1
                if isinstance(self.map[i][j], grass):
                    num_grass += 1
                if isinstance(self.map[i][j], tree):
                    num_tree += 1
                if isinstance(self.map[i][j], fire):
                    num_fire += 1
        #self.statistics.append((num_sheep, num_wolf))
        self.sheep_statistics.append(num_sheep)
        self.wolf_statistics.append(num_wolf)
        self.grass_statistics.append(num_grass)
        self.tree_statistics.append(num_tree)
        self.fire_statistics.append(num_fire)
        #return num_sheep, num_wolf

    #Goes through every block on the board in order to determine what said block should do this cycle
    #for every block it gets the view that block can see and calls the block's cycle function which is what decides what action will be taken

    def next_cycle(self, round):
        # keeps track of which sheep have been moved this cycle so that a sheep does not get stuck in a loop of cycling
        moved = []
        #self.c.create_rectangle(0, 0, 0+TILE_SIZE, 0+TILE_SIZE, fill = "yellow")
        for i in range (0, self.rows, TILE_SIZE):
            for j in range (0, self.cols, TILE_SIZE):
                r = self.map[i][j].range
                view = self.radius_around_coord(i, j, r)
                old_tile = self.map[i][j]
                if self.map[i][j] not in moved:
                    new_tile = self.map[i][j].cycle(view, round)
                if new_tile != None:
                    # handles moving entities
                    if new_tile[2].movable == True and new_tile[2] not in moved:
                        # sets the sheeps new tile_on as what the tile used to be before the sheep
                        new_tile[2].tile_on = self.map[new_tile[0]][new_tile[1]]
                        # we need to update the new tile it moved to
                        self.map[new_tile[0]][new_tile[1]] = new_tile[2]
                        self.update_block(new_tile[0], new_tile[1])
                        if isinstance(new_tile[2], sheep) and isinstance(old_tile, sheep) or isinstance(new_tile[2], wolf) and isinstance(old_tile, wolf):
                            if i == new_tile[0] and j == new_tile[1]: #This check stops a sheep from consuming itself if it chooses a move of 0,0
                                continue
                            self.map[i][j] = old_tile.consume()[2] #replaces old location with dirt
                            self.update_block(i, j)
                            moved.append(new_tile[2])
                    else: #handles static entities
                        self.map[i][j] = new_tile[2] #we are using the [2] index to get the new object. [0] and [1] contain the x and y coords
                        self.update_block(i, j)
        self.update_weather()
        print(self.stats())

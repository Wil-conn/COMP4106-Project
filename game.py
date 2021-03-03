import tkinter
import numpy as np
from dirt_class import dirt

class gameboard():
    def __init__(self, x, y, c):
        self.cols = x
        self.rows = y
        self.map = np.empty((self.cols, self.rows), dtype = object)
        self.c = c

    #goes through every block in the array and draws it on screen according to its colour. every block has a size of 5x5 pixels
    def display(self):
        for i in range (0, self.rows, 5):
            for j in range (0, self.cols, 5):
                self.c.create_rectangle(i, j, i+5, j+5, fill = self.map[i][j].colour)

    #adds a cell to the board. right now it only adds dirt
    def add_cell(self, x, y):
        self.map[x][y] = dirt(x, y)

    #fills the board with dirt. used for when game is being initialize
    def fill_board(self):
        print("test")
        for i in range (0, self.rows, 5):
            for j in range (0, self.cols, 5):
                self.add_cell(i, j)

    #this returns an NxN array which contains all the objects in a radius R around a given block
    #this is used for determining what said block is able to "see"
    #ex: a dirt block only has knowledge of the blocks 1 block away from it, so it has an R of 1 and will return a 3x3 array of objects around it
    def radius_around_coord(self, x, y, r):
        view = np.empty(((r*2)+1, (r*2)+1), dtype = object)
        rows, cols = 0, 0

        for i in range (-(r*5), (r*5+1), 5):
            for j in range (-(r*5), (r*5+1), 5):
                if (x + i >= 0 and y + j >= 0) and (x + i < self.rows and y + j < self.cols):
                    view[rows][cols] = self.map[x+i][y+j]
                    cols += 1
                else:
                    view[rows][cols] = None
                    cols += 1
            rows += 1
            cols = 0

        return view

    #Goes through every block on the board in order to determine what said block should do this cycle
    #for every block it gets the view that block can see and calls the block's cycle function which is what decides what action will be taken
    def next_cycle(self, round):
        for i in range (0, self.rows, 5):
            for j in range (0, self.cols, 5):
                r = self.map[i][j].range
                view = self.radius_around_coord(i, j, r)
                new_tile = self.map[i][j].cycle(view, round)
                if new_tile != None:
                    self.map[i][j] = new_tile[2] #we are using the [2] index to get the new object. [0] and [1] contain the x and y coords

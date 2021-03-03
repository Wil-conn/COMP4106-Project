import tkinter
import numpy as np
from numpy import random
from game import gameboard
import time

GAME_SIZE = 400

def main():

    #setting up the tkinter canvas
    root = tkinter.Tk()
    c = tkinter.Canvas(root, bg="black", height = GAME_SIZE, width = GAME_SIZE)
    c.pack()

    #creates the board object
    board = gameboard(GAME_SIZE, GAME_SIZE, c)
    board.fill_board()
    round = 0
    while(1):
        board.next_cycle(round)
        board.display()
        root.update_idletasks()
        root.update()
        round += 1

if __name__ == "__main__":
    main()

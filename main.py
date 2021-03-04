import tkinter
import numpy as np
from numpy import random
from game import gameboard
import time
import profile

GAME_SIZE = 500
def main():

    #setting up the tkinter canvas
    root = tkinter.Tk()
    c = tkinter.Canvas(root, bg="black", height = GAME_SIZE, width = GAME_SIZE)
    c.pack()

    #creates the board object
    board = gameboard(GAME_SIZE, GAME_SIZE, c)
    board.fill_board()
    round = 0
    board.display()
    while(1):
        start = time.time()
        board.next_cycle(round)
        #board.display()
        root.update_idletasks()
        root.update()
        round += 1
        print("cycle number " + str(round) + " took " + str(time.time() - start))

if __name__ == "__main__":
    #profile.run('main()')
    main()

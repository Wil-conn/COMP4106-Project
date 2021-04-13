import tkinter
import numpy as np
from numpy import random
from game import gameboard
import time
import profile
import settings
import sys
from settings import GAME_SIZE
import matplotlib.pyplot as plt

def main():
    #setting up the tkinter canvas
    stats = False
    if len(sys.argv) == 2:
        stats = True

    root = tkinter.Tk()
    c = tkinter.Canvas(root, bg="black", height = GAME_SIZE+50, width = GAME_SIZE)
    c.pack()

    #creates the board object
    board = gameboard(GAME_SIZE, GAME_SIZE, c)
    board.fill_board()
    round = 0
    board.display()
    while(1):
        print("CYCLE NUMBER: "+str(round))
        start = time.time()
        board.next_cycle(round)
        #board.display()
        root.update_idletasks()
        root.update()
        round += 1
        #time.sleep(0.5)
        #x = input("Press Enter to continue...")
        if board.wolf_statistics[round-1] == 0 and board.sheep_statistics[round-1] == 0:
            break
        #if x == 'Q':
        #    break
        print("cycle number " + str(round) + " took " + str(time.time() - start))
    if stats is True:
        plt.plot(board.sheep_statistics, label="sheep population")
        plt.plot(board.wolf_statistics, label="wolf population")
        plt.plot(board.grass_statistics, label="grass stats")
        plt.plot(board.tree_statistics, label="tree stats")
        plt.plot(board.fire_statistics, label="fire stats")
        plt.legend(loc="upper left")
        plt.show()
if __name__ == "__main__":
    #profile.run('main()')
    main()

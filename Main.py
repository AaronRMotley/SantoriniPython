import tkinter as tk
import numpy as np
import Worker
import CellState

#BoardPieces
levelone,leveltwo,levelthree,domes = 22,18,14,18
#Other statics
playerpieces,boardsize = 2, 5
edge = boardsize-1
spacing = 5
header = (" "*(spacing+1)).join([" ", "A", "B", "C", "D", "E"])

def printboard(b):
    row, s = 1, ''
    for r in b:
        s += str(row)+(" "*spacing)
        for c in r:
            s += "L"+str(c.level)
            if c.occupied == True:
                s+= "-"+str(c.workerid)+(" "*(spacing-2))
            else:
                s += (" "*spacing)
        s += '\n'
        row += 1
    print(header)
    print(s)

#create board [[object] * rows] * columns
#board = [[CellState.Cell()] * boardsize] * boardsize -- This is wrong - makes pointers to existing cell objects
board = [[CellState.Cell()]*boardsize for n in range(boardsize)]
for r in range(len(board)):
    for c in range(len(board)):
        if r == 0 or r == edge or c == 0 or c == edge:
            board[c][r] = CellState.Cell(perimeter=True)

board[0][0].occupied = True
board[0][0].workerid = 1

count = 1
for r in board:
    for c in r:
        #print(c.getvariablestoprint())
        print(c.getvariables())
        #print([count, "--", "level", c.level, "occupied", c.occupied, "dome", c.dome, "perimeter", c.perimeter, "workerid", c.workerid])
        #print([count, "--", "level", c.level, "occupied", c.occupied, "dome", c.dome, "perimeter", c.perimeter, "workerid", c.workerid])
        #print([count, "--", "level", c.level, "occupied", c.occupied, "dome", c.dome, "perimeter", c.perimeter, "workerid", c.workerid])
        count += 1



#printboard(board)
#add pieces

#import tkinter as tk
import Worker as wk
import CellState as cs
import Board as bd
import Player as pl

PLAYER_COUNT = 2

main = bd.BoardManager()
player1 = pl.Player("G")
for x in range(PLAYER_COUNT):
    player1.workers.append(wk.Worker())
player2 = pl.Player("R")
for x in range(PLAYER_COUNT):
    player2.workers.append(wk.Worker())
print(main)

print(player1.workers[0])

main.add_worker(player1.workers[0], 1, 1)
print(main)
main.add_worker(player1.workers[1], 1, 2)
print(main)
main.add_worker(player2.workers[0], 3, 4)
print(main)
main.add_worker(player2.workers[1], 5, 5)



#               Main.py
#             /         \
#       Board ---------- Player  ---- God
#        /              /
#     Cell             /
#                     /
#                Worker

#import tkinter as tk
import Board as bd
import Player as pl

PLAYER_COUNT = 2

main = bd.BoardManager()

player1 = pl.Player("G")
player2 = pl.Player("R")

main.add_worker(player1.workers[0], 1, 1)
main.add_worker(player1.workers[1], 3, 5)
main.add_worker(player2.workers[0], 2, 2)
main.add_worker(player2.workers[1], 5, 5)

print(main)




#               Main.py
#             /         \
#       Board ---------- Player  ---- God
#        /              /
#     Cell             /
#                     /
#                Worker

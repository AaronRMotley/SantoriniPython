#import tkinter as tk
import Worker as worker
import CellState as cells
import Board as b
import Player as Player

player_worker_max, player_count = 2, 2
main = b.BoardManager()
print(main)


#               Main.py
#             /         \
#       Board ---------- Player  ---- God
#        /              /
#     Cell             /
#                     /
#                Worker

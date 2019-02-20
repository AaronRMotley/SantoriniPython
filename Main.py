# import tkinter as tk
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

# TODO check valid moves for a players


print(main)


#               Main.py
#             /         \
#       Board <-------- Player <---- God
#        /              /
#     Cell             /
#                     /
#                Worker
#
# Setup
# 1) Select Number of Players
# 2) Setup Players (and select God by random or choice)
# 3) First Player places both workers, then the second, then the third.
# 
# Turn Order
# 1) Check valid worker moves 
# 2) Move one worker (or both if God ability allows) --- CHECK FOR WIN CONDITION AT LEVEL 3
# 3) build with one worker (or both if God ability allows)
# 4) Do any post turn God abilities
# 5) Next player's turn

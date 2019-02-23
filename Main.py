# import tkinter as tk
import Board as bd

PLAYER_COUNT, WORKER_COUNT = 2, 2
PLAYER1, PLAYER2, PLAYER3 = 'R', 'G', 'B'

cur_player = PLAYER1

main = bd.BoardManager()
main.add_worker(cur_player, 5, 5)
main.add_worker(cur_player, 1, 1)
print(main)
print(main.valid_moves(cur_player))


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

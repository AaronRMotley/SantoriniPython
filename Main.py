# import tkinter as tk
import Board as bd

PLAYER_COUNT, WORKER_COUNT = 2, 2
PLAYER1, PLAYER2, PLAYER3 = 'R', 'G', 'B'

board = bd.BoardManager(board_size=5)
board.add_worker(PLAYER1, 1, 1)
board.add_worker(PLAYER2, 2, 3)

print(board)
board.move_worker(PLAYER1, 1, 1, 2, 1)
print(board)



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

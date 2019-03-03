# import tkinter as tk
import Board as bd
import InputVerification as iv
import utils

PLAYER1 = {'color':'R','name':'Player 1','team':1}
PLAYER2 = {'color':'B','name':'Player 2','team':2}
PLAYER3 = {'color':'G','name':'Player 3','team':1}
PLAYER4 = {'color':'Y','name':'Player 4','team':2}
PLAYER_LIST = [PLAYER1, PLAYER2, PLAYER3, PLAYER4]
WORKER_COUNT = 2

no_winner = True
players_turn = 0

# cur_player = PLAYER1
# main = bd.BoardManager()
# main.add_worker(cur_player, 5, 5)
# main.add_worker(cur_player, 1, 1)
# print(main)
# moves = main.valid_moves(cur_player)

player_count = iv.InputPlayerCount()
main = bd.BoardManager()

players_placed = 0
while players_placed < player_count:
    current_player = PLAYER_LIST[players_placed]
    work_count = 0
    while work_count < WORKER_COUNT:
        print(main)
        print('\n'+current_player['name'])
        placement = iv.InputWorkerPlace(main, current_player)
        #main.add_worker(current_player, placement[0], placement[1])
        utils.ClearScreen()
        work_count +=1
    players_placed += 1
print(main)


while no_winner:
    # TODO move workers and build testing
    players_turn += 1
    current_player = PLAYER_LIST[players_turn%player_count]

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

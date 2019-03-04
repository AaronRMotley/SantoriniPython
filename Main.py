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
player_turn = 0

# 2 and 3 player games are solo, but 4 player games have 2 teams
player_count = iv.InputPlayerCount()
main = bd.BoardManager()

# Each player (in order) plays their 2 piececs on the board, then the next player,
# until all players have placed their 2 workers
players_placed = 0
while players_placed < player_count:
    current_player = PLAYER_LIST[players_placed]
    work_count = 0
    while work_count < WORKER_COUNT:
        print(main)
        print('\n'+current_player['name'])
        # iv will grab input and modify the board
        iv.InputWorkerPlace(main, current_player)
        utils.ClearScreen()
        work_count +=1
    players_placed += 1
print(main)


while no_winner:
    # TODO move workers and build testing
    # Advance Player Turn
    player_turn += 1
    current_player = PLAYER_LIST[player_turn%player_count]
    print(f"{current_player['name']} turn")
    

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

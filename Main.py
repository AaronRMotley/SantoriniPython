# import tkinter as tk
import Board as bd
import InputVerification as iv
import utils
import tkinter as tk

PLAYER1 = {'color':'R','number':1,'name':'Player 1','team':1,'god':'','fullcolor':'Red'}
PLAYER2 = {'color':'B','number':2,'name':'Player 2','team':2,'god':'','fullcolor':'Blue'}
PLAYER3 = {'color':'G','number':3,'name':'Player 3','team':1,'god':'','fullcolor':'Green'}
#Player 4 only in team game version
PLAYER4 = {'color':'B','number':4,'name':'Player 4','team':2,'god':'','fullcolor':'Blue'}
PLAYER_LIST = [PLAYER1, PLAYER2, PLAYER3, PLAYER4]
WORKER_COUNT = 2

no_winner, turn = True, 0

# --------------------------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------------------


def getPlayerCount(gameboard = True):
    """gameboard =  True for GUI, False for text"""
    if gameboard == True:
        #TODO make tkinter message
        pass
    else:
        count = iv.InputPlayerCount()
    if count == 4:
        PLAYER_LIST[2] = {'color':'R','number':3,'name':'Player 3','team':1,'god':'','fullcolor':'Red'}
    return count
    

main = bd.BoardManager()
player_count = getPlayerCount()


players_placed = 0
while players_placed < player_count:
    current_player = PLAYER_LIST[players_placed]
    work_count = 0
    while work_count < WORKER_COUNT:
        print(main)
        print('\n'+current_player['name']+' -- '+current_player['fullcolor'])
        # iv asks for input and modify the board based on input
        iv.InputWorkerPlace(main, current_player, work_count+1)
        utils.ClearScreen()
        work_count +=1
    players_placed += 1
print(main)

# START GAME BASIC Terminal based
current_player = PLAYER1
while no_winner:
    utils.ClearScreen()
    print(main)
    print(f"{current_player['name']} ({current_player['fullcolor']}) turn")
    valid_moves = main.valid_moves(current_player)
    print(f'valid moves:\n{main.valid_moves_pretty_print(valid_moves)}')
    move = iv.InputWorkerMove(main, current_player, valid_moves=valid_moves)
    if main.check_winner(current_player):
        print(f"{current_player['name']} WINS")
        break
    utils.ClearScreen()
    print(main)
    valid_builds = main.valid_builds(current_player)
    print(f"valid build:{valid_builds}")
    build = iv.InputBuild(main, current_player, last_move=move, valid_builds=valid_builds)
    # Advance Player Turn
    turn += 1
    current_player = PLAYER_LIST[turn%player_count]
    main.end_turn(current_player)

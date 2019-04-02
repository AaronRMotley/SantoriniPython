import Board as bd
from os import system, name 
import utils

# Game board is fixed length of 5 spaces wide and long
INPUTS = ['A','a','B','b','C','c','D','d','E','e','1','2','3','4','5']
STR_TO_NUM = {'A':1,'a':1,'1':1,'B':2,'b':2,'2':2,'C':3,'c':3,'3':3,'D':4,'d':4,'4':4,'E':5,'e':5,'5':5}
NUM_TO_STR = {1:'A',2:'B',3:'C',4:'D',5:'E'}
DISPLAY_OFFSET = 1

def InputPlayerCount(prompt = "How many players? (2-4)"):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if value < 2 or value > 4:
            print("Only 2-4 player game")
            continue
        else:
            break
    return value

def InputWorkerPlace(main, current_player, worker_num, prompt = "Select an empty row and column to place a worker: "):
    while True:
        inputs = GetRowColInputs(prompt)
        if main.add_worker(current_player, inputs[0], inputs[1], worker_num):
            break
        else:
            print(f'Worker already in space {inputs[0]+DISPLAY_OFFSET}{NUM_TO_STR[inputs[1]+DISPLAY_OFFSET]}')
            continue

def InputWorkerMove(main, player):
    while True:
        valid_moves = main.valid_moves(player)
        move = GetRowColInputs("Select a worker to move: ") 
        if move in main.player_pieces(player):
            move += GetRowColInputs("Select a location to move to: ")
            print(move)
            print(valid_moves)
            if move in valid_moves:    
                if main.move_worker(player, move, valid_moves=valid_moves):
                    break
                else:
                    print("failed call to main.move_worker")
                    continue
            else: 
                printmove = [x+1 for x in move]
                print(f"Not a valid move {printmove}")
                continue
        else:
            printmove = [x+1 for x in move]
            if 'worker' in main.board[move[0]][move[1]]:
                print(f"Not your worker at {printmove}")
            else:
                print(f"No worker at {printmove}")

def InputBuild(main, player):
    while True: 
        valid_builds = main.valid_builds(main, player)
        


def GetRowColInputs(prompt, fail_message = "Input is not valid. Input Row and Column. Example Valid inputs: 2c"):
    while True:
        try:
            inputs = list(input(prompt))
            if len(inputs) <= 1 or len(inputs) > 2:
                print(fail_message)
                continue
            inputs[0] = str(inputs[0])
            inputs[1] = str(inputs[1])
            if not inputs[0] in INPUTS or not inputs[1] in INPUTS:
                print(fail_message)
                continue
            else:
                inputs[0], inputs[1] = STR_TO_NUM[inputs[0]]-DISPLAY_OFFSET, STR_TO_NUM[inputs[1]]-DISPLAY_OFFSET
                break
        except ValueError:
            print(fail_message)
            continue
    return inputs

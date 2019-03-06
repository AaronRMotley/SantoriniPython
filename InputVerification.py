import Board as bd
from os import system, name 

# Game board is fixed length of 5 spaces wide and long
INPUTS = ['A','a','B','b','C','c','D','d','E','e','1','2','3','4','5']
STR_TO_NUM = {'A':1,'a':1,'1':1,'B':2,'b':2,'2':2,'C':3,'c':3,'3':3,'D':4,'d':4,'4':4,'E':5,'e':5,'5':5}
NUM_TO_STR = {1:'A',2:'B',3:'C',4:'D',5:'E'}

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
        value = GetRowColInputs(prompt)
        if 'worker' in main.board[value[0]-1][value[1]-1]:
            print(f'Worker already in space {value[0]}{NUM_TO_STR[value[1]]}')
            continue
        else:
            main.add_worker(current_player, value[0], value[1], worker_num)
            break
    return value

def InputWorkerMove(main, player, prompt = "Select a worker to move: "):
    while True:
        selected = GetRowColInputs(prompt)
        if ( 'worker' in main.board[selected[0]-1][selected[1]-1]
        and main.board[selected[0]][selected[1]]['worker']['player'] == player):
            destination = GetRowColInputs("Select a location to move to: ")
            if destination in main.valid_moves(player):
                if main.move_worker(player, selected[0], selected[1], destination[0], destination[1]):
                    break
                else:
                    print("failed call to main.move_worker")
                    continue
            else:
                print(f"{destination[0]}{NUM_TO_STR[destination[1]]} is not a valid destination")
        else: 
            print(f"Not a valid worker for {player['name']}")
            continue

def GetRowColInputs(prompt, fail_message = "Input is not valid. Example Valid inputs: 1a, 11, A1, aA"):
    while True:
        try:
            value = list(input(prompt))
            if len(value) <= 1:
                print(fail_message)
                continue
            value[0] = str(value[0])
            value[1] = str(value[1])
            if not value[0] in INPUTS or not value[1] in INPUTS or not len(value) < 3:
                print(fail_message)
                continue
            else:
                value[0], value[1] = STR_TO_NUM[value[0]], STR_TO_NUM[value[1]]
                break

        except ValueError:
            print(fail_message)
            continue
    return value

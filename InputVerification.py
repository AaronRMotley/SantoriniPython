import Board as bd
from os import system, name 

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
            print(f'Worker already in space {inputs[0]+DISPLAY_OFFSET}{NUM_TO_STR[inputs[1]+DISPLAY_OFFSET]}')
            continue
        else:
            break

def InputWorkerMove(main, player, prompt = "Select a worker to move: "):
    while True:
        selected = GetRowColInputs(prompt)
        if ( 'worker' in main.board[selected[0]][selected[1]]
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

def GetRowColInputs(prompt, fail_message = "Input is not valid. Input Row and Column. Example Valid inputs: 2c"):
    while True:
        try:
            inputs = list(input(prompt))
            if len(inputs) <= 1:
                print(fail_message)
                continue
            inputs[0] = str(inputs[0])
            inputs[1] = str(inputs[1])
            if not inputs[0] in INPUTS or not inputs[1] in INPUTS or not len(inputs) <= 2:
                print(fail_message)
                continue
            else:
                inputs[0], inputs[1] = STR_TO_NUM[inputs[0]]-DISPLAY_OFFSET, STR_TO_NUM[inputs[1]]-DISPLAY_OFFSET
                break

        except ValueError:
            print(fail_message)
            continue
    return inputs

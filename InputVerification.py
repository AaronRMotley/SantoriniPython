import Board as bd
from os import system, name 

# Game board is fixed length of 5 spaces wide and long
ROW_INPUTS = [1, 2, 3, 4, 5]
COL_INPUTS = ['A','a','B','b','C','c','D','d','E','e']
COL_TRANSLATION_TO_NUM = {'A':1,'a':1,'B':2,'b':2,'C':3,'c':3,'D':4,'d':4,'E':5,'e':5}
COL_TRANSLATION_TO_STR = {1:'A',2:'B',3:'C',4:'D',5:'E'}

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

def InputWorkerPlace(board, prompt = "Select an empty row and column to place a worker: "):
    while True:
        value = SanitizeRowColInputs(prompt)
        if 'worker' in board[value[0]-1][value[1]-1]:
            print(f'Worker already in space {value[0]}{COL_TRANSLATION_TO_STR[value[1]]}')
            continue
        else:
            break
    return value

def InputWorkerMove(board, prompt = "Select a worker to move:"):
    pass

def SanitizeRowColInputs(prompt, basic_fail = "Input is not valid. Example Valid input: 1A"):
    while True:
        try:
            value = list(input(prompt))
            if len(value) <= 1:
                print(basic_fail)
                continue
            value[0] = int(value[0])
            value[1] = str(value[1])
            if not value[0] in ROW_INPUTS or not value[1] in COL_INPUTS or not len(value) < 3:
                print(basic_fail)
                continue
            else:
                value[1] = COL_TRANSLATION_TO_NUM[value[1]]

        except ValueError:
            print(basic_fail)
            continue
    return value

def ClearScreen():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
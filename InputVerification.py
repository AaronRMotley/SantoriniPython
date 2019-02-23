import Board as bd
from os import system, name 

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

def InputWorkerPlaceRow(prompt = "Select an empty row and column to place a worker: "):
    while True:
        try:
            value = list(input(prompt))
            value[0] = int(value[0])
            value[1] = str(value[1])
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if not value[0] in ROW_INPUTS and not value[1] in COL_INPUTS:
            print("Input is not valid, Select Row, Col. Valid input = 1A")
            continue
        else:
            # TODO Check the board to see if the move is valid
            break
    value[1] = COL_TRANSLATION_TO_NUM[value[1]]
    return value

def ClearScreen():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 
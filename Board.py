import CellState as cs
import Worker as wk
import Player as pl

# BoardPieces
LEVEL_ONE,LEVEL_TWO,LEVEL_THREE,DOMES = 22,18,14,18
WORKER_MAX = 2
# Other stats
PRINT_SPACING = 5

class BoardManager:
    def __init__(self, board_size = 5):
        self.board = [[(cs.Cell(), '') for n in range(board_size)] for x in range(board_size)]
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if r == 0 or r == (board_size-1) or c == 0 or c == (board_size-1):
                    self.board[c][r][0].perimeter = True
    
    def add_worker(self, worker, row, column):
        if self.board[row-1][column-1][0].occupied != True:
            self.board[row-1][column-1] = (self.board[row-1][column-1][0], worker)
            self.board[row-1][column-1][0].occupied = True
        else:
            return "Space is occupied"

    def valid_moves(self, player):
        #TODO
        pass

    def move_worker(self, worker, row, column):
        #TODO
        pass
    
    def endturn(self):
        #TODO
        pass
    
    def __str__(self):
        #header = (" "*(PRINT_SPACING+1)).join([" ", "A", "B", "C", "D", "E"])
        row, s = 1, (" "*(PRINT_SPACING+1)).join([" ", "A", "B", "C", "D", "E"])
        for r in self.board:
            s += '\n'+str(row)+(" "*PRINT_SPACING)
            for c in r:
                s += "L"+str(c[0].level)
                if c[0].occupied == True:
                    s+= "-"+str(c[1]) + str(c[1]) +(" "*(PRINT_SPACING-2))
                else:
                    s += (" "*PRINT_SPACING)
            #s += '\n'
            row += 1
        return s
import Player as pl

# BoardPieces
LEVEL_ONE,LEVEL_TWO,LEVEL_THREE,DOMES = 22,18,14,18
WORKER_MAX = 2
# Other stats
PRINT_SPACING = 5
NULL = ''

class BoardManager:
    def __init__(self, board_size = 5):
        self.board = [[(Cell()) for n in range(board_size)] for x in range(board_size)]
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if r == 0 or r == (board_size-1) or c == 0 or c == (board_size-1):
                    self.board[c][r].perimeter = True

    def add_worker(self, worker, row, column):
        if row < 1 or row > 5 or column < 0 or column > 5:
            return "invalid inputs"
        if self.board[row-1][column-1].worker == NULL:
            self.board[row-1][column-1].worker = worker
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
                s += "L"+str(c.level)
                if c.worker != NULL:
                    s+= "-"+str(c.worker.color) + str(c.worker.id) +(" "*(PRINT_SPACING-3))
                else:
                    s += (" "*PRINT_SPACING)
            #s += '\n'
            row += 1
        return s


class Cell:
    def __init__(self, perimeter = False):
        self.level = 0
        self.dome = False
        self.perimeter = perimeter
        self.worker = NULL
        
    def build(self):
        if self.level < 4:
            self.level += 1
        if self.level >= 4:
            self.dome = True

    # Used only by God of war
    def destroy(self):
        if self.level > 0 and self.dome != True:
            self.level -= 1
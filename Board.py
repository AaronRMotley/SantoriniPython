import CellState as cells
import Worker as worker
import Player as player

# BoardPieces
LEVELONE,LEVELTWO,LEVELTHREE,DOMES = 22,18,14,18
# Other stats
PRINTSPACING = 5

class BoardManager:
    def __init__(self, boardsize = 5):
        #board = [[CellState.Cell()] * boardsize] * boardsize -- This is wrong - makes pointers to existing cell objects
        self.board = []
        count = boardsize
        while count > 0:
            self.board.append([(cells.Cell(), '') for n in range(boardsize)])
            count -= 1
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if r == 0 or r == (boardsize-1) or c == 0 or c == (boardsize-1):
                    self.board[c][r][0].perimeter = True
    
    def add_worker(self, player, row, column):
        #TODO
        pass

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
        #header = (" "*(PRINTSPACING+1)).join([" ", "A", "B", "C", "D", "E"])
        row, s = 1, (" "*(PRINTSPACING+1)).join([" ", "A", "B", "C", "D", "E"])
        for r in self.board:
            s += '\n'+str(row)+(" "*PRINTSPACING)
            for c in r:
                s += "L"+str(c[0].level)
                if c[0].occupied == True:
                    #TODO Write new login
                    pass
                    #s+= "-"+str(c[1].player) + str(c[1].id) +(" "*(PRINTSPACING-2))
                else:
                    s += (" "*PRINTSPACING)
            #s += '\n'
            row += 1
        return s
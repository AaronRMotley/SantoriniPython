import CellState as cells
import Worker as work

#BoardPieces
levelone,leveltwo,levelthree,domes = 22,18,14,18
#Other stats
boardsize = 5
playerpiecesmax, playercount = 2, 2
printspacing = 5

class BoardManager:
    def __init__(self):
        #board = [[CellState.Cell()] * boardsize] * boardsize -- This is wrong - makes pointers to existing cell objects
        self.board = []
        count = boardsize
        while count > 0:
            self.board.append([(cells.Cell(), work.Worker()) for n in range(boardsize)])
            count -= 1
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if r == 0 or r == (boardsize-1) or c == 0 or c == (boardsize-1):
                    self.board[c][r][0].perimeter = True
        self.workers = []

    def addworker(self, player):
        pass

    def moveworker(self, workerid):
        pass
    
    def printboard(self):
        #header = (" "*(printspacing+1)).join([" ", "A", "B", "C", "D", "E"])
        row, s = 1, (" "*(printspacing+1)).join([" ", "A", "B", "C", "D", "E"])
        for r in self.board:
            s += '\n'+str(row)+(" "*printspacing)
            for c in r:
                s += "L"+str(c[0].level)
                if c[0].occupied == True:
                    s+= "-"+str(c[0].workerboardprint())+(" "*(printspacing-2))
                else:
                    s += (" "*printspacing)
            #s += '\n'
            row += 1
        return s


    


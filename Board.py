import Player as pl

# BoardPieces
LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, DOMES = 22, 18, 14, 18
WORKER_MAX = 2
# Other stats
PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E"]
NULL = ''

current_player = pl.Player('fake')


class BoardManager:
    def __init__(self, board_size=5):
        ends = board_size-1
        self.board = [[(Cell()) for n in range(board_size)] for x in range(board_size)]
        for r in range(ends):
            for c in range(ends):
                if r == 0 or r == (ends) or c == 0 or c == (ends):
                    self.board[c][r].perimeter = True

    def add_worker(self, worker, row, column):
        if row < 1 or row > 5 or column < 0 or column > 5:
            return "invalid inputs"
        if self.board[row-1][column-1].worker == NULL:
            self.board[row-1][column-1].worker = worker
        else:
            return "Space is occupied"
             
    def move_worker(self, worker, row, column):
        self.board[row-1][column-1].worker = worker

    def __str__(self):
        row, s = 1, (" "*(PRINT_SPACING+1)).join(HEADER)
        for r in self.board:
            s += '\n'+str(row)+(" "*PRINT_SPACING)
            for c in r:
                s += "L"+str(c.level)
                if c.worker != NULL:
                    s += "-" + str(c.worker.color) + str(c.worker.id) + (" "*(PRINT_SPACING-3))
                else:
                    s += (" "*PRINT_SPACING)
            row += 1
        return s


class Cell:
    def __init__(self, perimeter=False):
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
        if self.level > 0 and self.dome:
            self.level -= 1

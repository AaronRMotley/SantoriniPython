# BoardPieces Max
LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, DOMES = 22, 18, 14, 18
# Other stats for Printing
PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E"]

# Example Board cell dictionary
# {'level': 0, 'dome': False, 'perimeter': False, 'worker': {'moved': False, 'ascended': False, 'player': 'R'}}

class BoardManager:
    def __init__(self, board_size=5):
        ends = board_size-1
        self.board = [[{'level': 0, 'dome': False, 'perimeter': False} for n in range(board_size)] for x in range(board_size)]
        for r in range(ends):
            for c in range(ends):
                if r == 0 or r == (ends) or c == 0 or c == (ends):
                    self.board[r][c]['perimeter'] = True

    def add_worker(self, player, row, column):
        if row < 1 or row > 5 or column < 0 or column > 5:
            return "invalid inputs"
        if 'worker' not in self.board[row-1][column-1]:
            self.board[row-1][column-1]['worker'] = {'moved': False, 'ascended': False, 'player': player}
        else:
            return "Space is occupied"
             
    def move_worker(self, player, old_row, old_col, new_row, new_col):
        if 'worker' in self.board[old_row-1][old_col-1] and 'worker' not in self.board[new_row-1][new_col-1] \
              and player == self.board[old_row-1][old_col-1]['worker']['player']:
            self.board[new_row-1][new_col-1]['worker'] = self.board[old_row-1][old_col-1]['worker']
            del(self.board[old_row-1][old_col-1]['worker'])

    def build(self, row, col):
        if self.board[row-1][col-1]['level'] < 4:
            self.board[row-1][col-1]['level'] += 1
        if self.board[row-1][col-1]['level'] >= 4:
            self.board[row-1][col-1]['dome'] = True

    def __str__(self):
        row, s = 1, (" "*(PRINT_SPACING+1)).join(HEADER)
        for r in self.board:
            s += '\n'+str(row)+(" "*PRINT_SPACING)
            for c in r:
                if c['dome'] == True or c['level'] >= 4:
                    s+= "D^"
                else:
                    s += "L"+str(c['level'])
                if 'worker' in c:
                    s += "-" + str(c['worker']['player']) + (" "*(PRINT_SPACING-2))
                else:
                    s += (" "*PRINT_SPACING)
            row += 1
        return s+'\n'


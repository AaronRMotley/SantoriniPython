# BoardPieces Statics
BOARD_SIZE = 5
LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, DOMES = 22, 18, 14, 18
# Other stats for Printing
PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E"]
# Example Board cell dictionary
# {'level': 0, 'dome': False, 'perimeter': False, 'worker': {'moved': False, 'ascended': False, 'player': {'color':'R','name':'Player 1','team':1}}}

class BoardManager:
    def __init__(self, player_count = 2):
        self.player_count = player_count
        ends = BOARD_SIZE-1
        self.board = [[{'level': 0, 'dome': False, 'perimeter': False} for n in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if r == 0 or r == (ends) or c == 0 or c == (ends):
                    self.board[r][c]['perimeter'] = True

    def add_worker(self, player, row, column, number):
        if row < 1 or row > 5 or column < 0 or column > 5:
            return "invalid inputs"
        if 'worker' not in self.board[row-1][column-1]:
            self.board[row-1][column-1]['worker'] = {'moved': False, 'ascended': False, 'player': player, 'number': number}
        else:
            return "Space is occupied"

    # Valid Moves returns a list containg [Dest_row, Dest_col, Origin_row, Origin_col] with numbers formatted
    # for board rows and columns with values between 1 and 5
    def valid_moves(self, player):
        valid_moves = []
        row = 0
        for r in self.board:
            col = 0
            for c in r:
                if 'worker' in c:
                    if c['worker']['player']['name'] == player['name'] or (c['worker']['player']['team'] == player['team'] and self.player_count == 4):
                        for test_row in range(row-1, row+2):
                            for test_col in range(col-1, col+2):
                                if ( test_row < BOARD_SIZE and test_col < BOARD_SIZE 
                                and test_row >= 0 and test_col >= 0 
                                and self.board[test_row][test_col]['dome'] != True 
                                and self.board[test_row][test_col]['level'] <= self.board[row][col]['level'] 
                                and not 'worker' in self.board[test_row][test_col] ):
                                    valid_moves.append([test_row+1, test_col+1, row+1, col+1])
                col += 1
            row += 1
        return valid_moves

    def valid_moves_pretty_print(self, valid_moves):
        NUM_TO_STR = {1:'A',2:'B',3:'C',4:'D',5:'E'}
        pretty_str = ''
        for x in valid_moves[:-1]:
            pretty_str += str(x[2]) + str(NUM_TO_STR[x[3]]) + '->' + str(x[0]) + str(NUM_TO_STR[x[1]]) + ', '
        else:
            pretty_str += str(valid_moves[-1][2]) + str(NUM_TO_STR[valid_moves[-1][3]]) + '->' + \
                str(valid_moves[-1][0]) + str(NUM_TO_STR[valid_moves[-1][1]])
        return pretty_str

    # Receive Row and Col inputs values 1-5, translation to list 0-4 is done here
    def move_worker(self, player, old_row, old_col, new_row, new_col):
        if ( 'worker' in self.board[old_row-1][old_col-1] and 'worker' not in self.board[new_row-1][new_col-1] 
              and player == self.board[old_row-1][old_col-1]['worker']['player'] ):
            self.board[new_row-1][new_col-1]['worker'] = self.board[old_row-1][old_col-1]['worker']
            del(self.board[old_row-1][old_col-1]['worker'])
            return True
        else: 
            return False

    def valid_builds(self, player):
        valid_builds = []
        row = 0
        for r in self.board:
            col = 0
            for c in r:
                if 'worker' in c:
                    if c['worker']['moved'] == True \
                    and (c['worker']['player']['name'] == player['name'] \
                    or (c['worker']['player']['team'] == player['team'] and self.player_count == 4)):
                        for test_row in range(row-1, row+2):
                            for test_col in range(col-1, col+2):
                                if test_row < BOARD_SIZE and test_col < BOARD_SIZE \
                                and test_row >= 0 and test_col >= 0 \
                                and self.board[test_row][test_col]['dome'] != True \
                                and not (row == test_row and col == test_col):
                                    valid_builds.append((test_row+1, test_col+1))
                col += 1
            row += 1
        return valid_builds

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
                    s += "-" + str(c['worker']['player']['color']) + str(c['worker']['number']) + (" "*(PRINT_SPACING-3))
                else:
                    s += (" "*PRINT_SPACING)
            row += 1
        return s+'\n'

    

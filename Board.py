# BoardPieces Statics
BOARD_SIZE = 5
LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, DOMES = 22, 18, 14, 18
# Other stats for Printing
PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E"]

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
        if 'worker' not in self.board[row][column]:
            self.board[row][column]['worker'] = {'moved':False,'ascended':False,'number':number,'player':player}
            return True
        else:
            return False

    # Valid Moves returns a list containg [Dest_row, Dest_col, Origin_row, Origin_col] with numbers formatted
    # for board rows and columns with values between 1 and 5
    def valid_moves(self, player):
        valid_moves = []
        row = 0
        for r in self.board:
            col = 0
            for c in r:
                if 'worker' in c:
                    if c['worker']['player'] == player or (c['worker']['player']['team'] == player['team'] and self.player_count == 4):
                        for dest_row in range(row-1, row+2):
                            for dest_col in range(col-1, col+2):
                                if ( 
                                dest_row < BOARD_SIZE and dest_row >= 0 and dest_col < BOARD_SIZE and dest_col >= 0 
                                and not 'worker' in self.board[dest_row][dest_col]
                                and self.board[dest_row][dest_col]['dome'] != True 
                                # must not go up more than 1 level but can drop down to ground always
                                and self.board[dest_row][dest_col]['level']-1 <= self.board[row][col]['level'] 
                                ):
                                    valid_moves.append([row, col, dest_row, dest_col])
                col += 1
            row += 1
        return valid_moves

    def valid_moves_pretty_print(self, valid_moves):
        if not valid_moves:
            return ''
        NUM_TO_STR = {0:'A',1:'B',2:'C',3:'D',4:'E'}
        pretty_str = ''
        for x in valid_moves[:-1]:
            pretty_str += str(x[0]+1) + str(NUM_TO_STR[x[1]]) + '->' + str(x[2]+1) + str(NUM_TO_STR[x[3]]) + ', '
        else:
            pretty_str += str(valid_moves[-1][0]+1) + str(NUM_TO_STR[valid_moves[-1][1]]) + '->' + \
                str(valid_moves[-1][2]+1) + str(NUM_TO_STR[valid_moves[-1][3]])
        return pretty_str

    # Receive Row and Col inputs values 1-5, translation to list 0-4 is done here
    def move_worker(self, player, old_row, old_col, new_row, new_col):
        if ( 'worker' in self.board[old_row][old_col] and 'worker' not in self.board[new_row][new_col] 
              and player == self.board[old_row][old_col]['worker']['player'] ):
            self.board[new_row][new_col]['worker'] = self.board[old_row][old_col]['worker']
            del(self.board[old_row][old_col]['worker'])
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
                    if (
                    c['worker']['moved'] == True 
                    and ( c['worker']['player']['name'] == player['name'] 
                    or (c['worker']['player']['team'] == player['team'] and self.player_count == 4) )
                    ):
                        for dest_row in range(row-1, row+2):
                            for dest_col in range(col-1, col+2):
                                if (
                                dest_row < BOARD_SIZE and dest_col < BOARD_SIZE 
                                and dest_row >= 0 and dest_col >= 0 
                                and self.board[dest_row][dest_col]['dome'] != True 
                                and not (row == dest_row and col == dest_col
                                ):
                                    valid_builds.append([dest_row, dest_col])
                col += 1
            row += 1
        return valid_builds

    def build(self, row, col):
        if self.board[row][col]['level'] < 4:
            self.board[row][col]['level'] += 1
        if self.board[row][col]['level'] >= 4:
            self.board[row][col]['dome'] = True

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

    def end_turn(self, next_player):
        for x in self.board:
            for y in x:
                if 'worker' in y:
                    y['worker']['moved'] = False
                    if y['worker']['player'] == next_player:
                        y['worker']['ascended'] = False

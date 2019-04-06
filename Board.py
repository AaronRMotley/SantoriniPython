from operator import itemgetter
from itertools import groupby

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

    def player_pieces(self, player):
        playerpieces = []
        row = 0
        for r in self.board:
            col = 0
            for c in r:
                if 'worker' in c:
                    if c['worker']['player'] == player or (c['worker']['player']['team'] == player['team'] and self.player_count == 4):
                        playerpieces.append([row, col])
                col += 1
            row += 1
        return playerpieces


    # Valid Moves returns a list containg [Dest_row, Dest_col, Origin_row, Origin_col] with numbers formatted
    # for board rows and columns with values between 1 and 5
    def valid_moves(self, player):
        playerpieces = self.player_pieces(player)
        valid_moves = []
        row = 0
        for r in self.board:
            col = 0
            for c in r:
                if 'worker' in c:
                    if [row, col] in playerpieces:
                        for dest_row in range(row-1, row+2):
                            for dest_col in range(col-1, col+2):
                                # Basic move without God attributes
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
        valid_moves = sorted(valid_moves, key=itemgetter(0,1))
        grouped_moves = groupby(valid_moves, itemgetter(0,1))
        for x in grouped_moves:
            pretty_str += str(x[0][0]+1) + str(NUM_TO_STR[x[0][1]]) + ' -> '
            for y in x[1]:
                pretty_str += str(y[2]+1) + str(NUM_TO_STR[y[3]]) + ','
            else:
                pretty_str = pretty_str[:-1]
                pretty_str += '\n'
        return pretty_str

    def move_worker(self, player, move, valid_moves = []):
        if not valid_moves:
            valid_moves = self.valid_moves(player)
        if move in valid_moves and len(move) == 4:
            self.board[move[2]][move[3]]['worker'] = self.board[move[0]][move[1]]['worker']
            del(self.board[move[0]][move[1]]['worker'])
            self.board[move[2]][move[3]]['worker']['moved'] = True
            # if moved up a level: ascended == True
            if self.board[move[0]][move[1]]['level'] < self.board[move[2]][move[3]]['level']:
                self.board[move[2]][move[3]]['worker']['ascended'] = True
            return True
        else: 
            return False

    def valid_builds(self, player):
        valid_builds = []
        playerpieces = self.player_pieces(player)
        row = 0
        for r in self.board:
            col = 0
            for c in r:
                if ( [row, col] in playerpieces and c['worker']['moved'] == True ):
                    for dest_row in range(row-1, row+2):
                        for dest_col in range(col-1, col+2):
                            # Normal build with no God attributes
                            if (
                            dest_row < BOARD_SIZE and dest_col < BOARD_SIZE 
                            and dest_row >= 0 and dest_col >= 0 
                            and self.board[dest_row][dest_col]['dome'] != True 
                            and self.board[dest_row][dest_col]['level'] < 4
                            and self.board[dest_row][dest_col]['level'] >= 0
                            and not (row == dest_row and col == dest_col)
                            and not 'worker' in self.board[dest_row][dest_col]
                            ):
                                valid_builds.append([dest_row, dest_col])
                col += 1
            row += 1
        return valid_builds

    def build(self, player, row, col, valid_builds= []):
        if not valid_builds:
            valid_builds = self.valid_builds(player)
        if [row, col] in valid_builds:
            self.board[row][col]['level'] += 1
            if self.board[row][col]['level'] >= 4:
                self.board[row][col]['dome'] = True
            return True
        else: # Not a valid build or problem with levels
            return False
        
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

    def end_turn(self, next_player, player_count=2):
        for r in self.board:
            for c in r:
                if 'worker' in c:
                    c['worker']['moved'] = False
                    if c['worker']['player'] == next_player:
                        c['worker']['ascended'] = False

    def check_winner(self, player):
        for r in self.board:
            for c in r:
                if 'worker' in c:
                    if c['level'] == 3:
                        return True
                    #Or special God Win
        else:
            return False


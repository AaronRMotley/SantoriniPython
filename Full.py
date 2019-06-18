import tkinter as tk
from operator import itemgetter
from itertools import groupby
from os import system, name 

PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U", "V", "W", "X", "Y", "Z"]


#Game statistic trackers
no_winner, turn = True, 0

###########################  Main Board Object ##################################
class BoardManager:
    def __init__(self, board_size = 5, lvl_one_pcs = 22, lvl_two_pcs = 18, lvl_three_pcs = 14, dome_pcs = 18, 
                team = False, team_mod = 2, player_count = 2, enable_gods = False, worker_max = 2):
        """ Inialize the board variable that is the main structure for workers and piece placement
            The Board contains all data about the current state of the game \n
            player_count between 2 and 4 players
            *_pcs are the count of available pieces of each type
            team game is True or False
            team mod sets the number of players per team, default 2
            worker_max per player - default 2
            """
        self.board_size = board_size
        self.lvl_one_pcs,self.lvl_two_pcs,self.lvl_three_pcs,self.dome_pcs = lvl_one_pcs,lvl_two_pcs,lvl_three_pcs,dome_pcs
        self.team, self.team_mod, self.player_count, self.enable_gods = team, team_mod, player_count, enable_gods
        self.worker_max = worker_max
        self.board = [[{'level': 0, 'dome': False, 'perimeter': False} for n in range(board_size)] for x in range(board_size)]
        for row_index in enumerate(self.board):
            for col_index in enumerate(self.board):
                if row_index == 0 or row_index == board_size-1 or col_index == 0 or col_index == board_size-1:
                    self.board[row_index][col_index]['perimeter'] = True

    def _add_worker(self, player, row, column):
        """Initial placement of workers. pass player and destination row and column"""
        number = len(self._player_pieces(player['id'])) + 1
        if 'worker' not in self.board[row][column]:
            self.board[row][column]['worker'] = {'moved':False,'ascended':False,'number':number,'player':player}
            return True
        else:
            return False

    def _player_pieces(self, player_id):
        """given the player['id'] of a player
        return a list of board coordinates where that players workers are located

        In Team games return all team members pieces as well
        """
        playerpieces = []
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if 'worker' in col:
                    if (col['worker']['player']['id'] == player_id or
                        (self.team == True and col['worker']['player']['id'] % self.team_mod == player_id % 2)):
                        playerpieces.append([row_index, col_index])
        return playerpieces
   
    def _valid_moves(self, player_id):
        """ Valid Moves returns a list containing [Origin_row, Origin_col, Dest_row, Dest_col, ] with numbers formatted
            for board rows and columns with values between 1 and 5
        """
        playerpieces = self._player_pieces(player_id)
        valid_moves = []
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                if 'worker' in cell and [row_index, col_index] in playerpieces:
                    for dest_row in range(row_index-1, row_index+2):
                        for dest_col in range(col_index-1, col_index+2):
                            # Basic move without God attributes
                            if ( 
                            dest_row < self.board_size and dest_row >= 0 and dest_col < self.board_size and dest_col >= 0 
                            and not 'worker' in self.board[dest_row][dest_col]
                            and self.board[dest_row][dest_col]['dome'] == False 
                            # must not go up more than 1 level but can drop down to ground always
                            and self.board[dest_row][dest_col]['level']-1 <= self.board[row_index][col_index]['level'] 
                            ):
                                valid_moves.append([row_index, col_index, dest_row, dest_col])
        return valid_moves

    def _move_worker(self, player_id, move, valid_moves = []):
        """Move Selected player piece to target destination
        
        format for a move variable are:
        move = list[start_row, start_col, new_row, new_col]
        valid_moves = list[move]

        returns true if piece is moved, false if not moved
        """
        if not valid_moves:
            valid_moves = self._valid_moves(player_id)
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

    def _valid_builds(self, player_id):
        valid_builds = []
        playerpieces = self._player_pieces(player_id)
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                if ([row_index, col_index] in playerpieces and cell['worker']['moved'] == True ):
                    for dest_row in range(row_index-1, row_index+2):
                        for dest_col in range(col_index-1, col_index+2):
                            # Normal build with no God attributes
                            if (
                            dest_row < self.board_size and dest_col < self.board_size 
                            and dest_row >= 0 and dest_col >= 0
                            and not (row_index == dest_row and col_index == dest_col)
                            and self.board[dest_row][dest_col]['dome'] == False 
                            and self.board[dest_row][dest_col]['level'] <= 3
                            and self.board[dest_row][dest_col]['level'] >= 0
                            and not 'worker' in self.board[dest_row][dest_col]
                            ):
                                valid_builds.append([dest_row, dest_col])
        return valid_builds

    def _build(self, player_id, row, col, valid_builds= []):
        """Given the player_id, row, and col of the build location
            returns true if built
            false if failed
        """
        if not valid_builds:
            valid_builds = self._valid_builds(player_id)
        if [row, col] in valid_builds:
            if self.board[row][col]['level'] == 3:
                self.board[row][col]['dome'] = True
            else:
                self.board[row][col]['level'] += 1
            return True
        else: # Not a valid build or problem with levels
            return False
        
    def _end_turn(self, next_player_id):
        for r in self.board:
            for c in r:
                if 'worker' in c:
                    c['worker']['moved'] = False
                    if c['worker']['player']['id'] == next_player_id:
                        c['worker']['ascended'] = False

    def _check_winner(self, player):
        """ check the board to see if a win condition as been done
        player is needed for special God rules, but not for vanilla game
        """
        for r in self.board:
            for c in r:
                if 'worker' in c:
                    if c['level'] == 3:
                        return True
                    #TODO Or special God Win
        else:
            return False

    def _check_winnable(self):
        if self.lvl_three_pcs <= 0:
            for row in self.board:
                for cell in row:
                    if cell['level'] == 3 and cell['dome'] == False:
                        return True
            else:
                return False
        else:
            return True

    def _valid_moves_pretty_print(self, valid_moves):
        if not valid_moves:
            return ''
        pretty_str = ''
        valid_moves = sorted(valid_moves, key=itemgetter(0,1))
        grouped_moves = groupby(valid_moves, itemgetter(0,1))
        for x in grouped_moves:
            pretty_str += str(x[0][0]+1) + ',' + str(x[0][1]+1) + ' ->'
            for y in x[1]:
                pretty_str += ' [' + str(y[2]+1) + ',' + str(y[3]+1) + '],'
            else:
                pretty_str = pretty_str[:-1]
                pretty_str += '\n'
        return pretty_str

    def __str__(self):
        s = (" "*(PRINT_SPACING+1)).join(HEADER[:self.board_size+1])
        for row_index, row in enumerate(self.board):
            s += '\n'+str(row_index+1)+(" "*PRINT_SPACING)
            for cell in row:
                if cell['dome'] == True:
                    s+= "D^"
                else:
                    s += "L"+str(cell['level'])
                if 'worker' in cell:
                    s += "-" + str(cell['worker']['player']['color_name'][0]) + str(cell['worker']['number']) + (" "*(PRINT_SPACING-3))
                else:
                    s += (" "*PRINT_SPACING)
        return s+'\n'

###########################  End Main Board Object ##################################

def _input_to_coordinate(max = 5, click_input = False, prompt = 'Enter comma seperated coordinate (ex. a,2): '):
    """Asks for input to coordinate.
        If click_input if set to True, will wait for click and validate. 
        If false, will ask for text input and validate. Will only accept values from 1 to max

        max default is 5
        click_input default is False

        Returns 2 values = Row, Col
    """
    if click_input:
        #TODO click input
        return []
    else:
        while (True):
            try:
                txt_list = input(f'{prompt}').split(',')
                if len(txt_list) == 2:
                    coordinate = []
                    for txt in txt_list:
                        txt = ''.join(char for char in txt if char.isalnum())
                        coordinate.append(int(''.join([str(ord(char)-96) 
                            if char != '' and not char.isdigit()
                            else char for char in txt.lower()])))               
                    for index,num in enumerate(coordinate):
                        if num < 1 or num > max:
                            raise Exception('value not on board')
                        else:
                            #Change coordinate from start 1 to start 0 for list management
                            coordinate[index] -= 1
                    else:
                        return coordinate[0], coordinate[1]
                else:
                    raise Exception('Not valid entry. Example: a,1')
            except Exception as e:
                print(e)
                continue

def _try_place_worker(main, current_player, is_gui = False):
    """ Initial placement of workers
        pass in the board and current player

        is_gui is False for text, True for Tkinter enabled

        returns True once able to place a worker successfully
        returns False if exception is caught. Possibly failing to place worker
    """
    while True:
        try: 
            row, col = _input_to_coordinate(max = main.board_size, click_input = is_gui, 
                prompt="Select an empty row and column to place a worker: ")
            if main._add_worker(current_player, row, col):
                return True
            else:
                print(f'Worker already in space {row + 1},{col + 1}')
                continue
        except Exception:
            return False

def _try_worker_move(main, player_id, valid_moves=[]):
    
    while True:
        try: 
            if not valid_moves:
                valid_moves = main._valid_moves(player_id)
            row, col = _input_to_coordinate(max=main.board_size, prompt="Select a worker to move: ") 
            move = [row, col]
            if move in main._player_pieces(player_id):
                row, col = _input_to_coordinate(max=main.board_size, prompt="Select a location to move to: ")
                move += [row, col]
                print(move)
                if move in valid_moves:    
                    if main._move_worker(player_id, move, valid_moves=valid_moves):
                        break
                    else:
                        raise Exception("failed to move worker")
                else: 
                    raise Exception("Not a valid move")
            else:
                if 'worker' in main.board[move[0]][move[1]]:
                    raise Exception("Not your worker")
                else:
                    raise Exception("No worker")
        except Exception as e:
            print(e)
            continue
    return move

def _try_build(main, player, valid_builds=[]):
    if not valid_builds:
        valid_builds = main._valid_builds(player)
    while True:
        row, col = _input_to_coordinate(max=main.board_size, prompt="Select a space to build: ")
        if main._build(player['id'], row, col, valid_builds):
            return True
        else:
            print(f"not a valid build spot {row+1} {col+1}")
            continue
    return build

def _create_player_list(is_gui = False):
    #TODO create ability to change player counts and player variables like color and gods
    PLAYER1 = {'id':1,'name':'Player 1','hex_color':'FF0000','god':'','color_name':'Red'}
    PLAYER2 = {'id':2,'name':'Player 2','hex_color':'0000FF','god':'','color_name':'Blue'}
    #PLAYER3 = {'id':3,'name':'Player 3','hex_color':'008000','god':'','color_name':'Green'}
    PLAYER_LIST = [PLAYER1, PLAYER2]
    return PLAYER_LIST, len(PLAYER_LIST)

def _clear_screen():
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

# --------------------------------------------------------------------------------------------
# Setup
# 1) Select Number of Players
# 2) Setup Players (and select God by random or choice)
# 3) First Player places both workers, then the second, then the third.
# 
# Turn Order
# 1) Check valid worker moves 
# 2) Move one worker (or both if God ability allows) --- CHECK FOR WIN CONDITION AT LEVEL 3
# 3) build with one worker (or both if God ability allows)
# 4) Do any post turn God abilities
# 5) Next player's turn
# ---------------------------------------------------------------------------------------------
main = BoardManager()
player_list, player_count = _create_player_list()

players_placed = 0
while players_placed < player_count:
    current_player = player_list[players_placed]
    work_count = 0
    while work_count < 2:
        print(main)
        print('\n'+current_player['name'])
        _try_place_worker(main, current_player)
        _clear_screen()
        work_count +=1
    players_placed += 1

# START GAME BASIC Terminal based
current_player = player_list[0]
while no_winner:
    _clear_screen()
    print(main)
    print(f"{current_player['name']} turn")
    valid_moves = main._valid_moves(current_player['id'])
    print(f'valid moves:\n{main._valid_moves_pretty_print(valid_moves)}')
    move = _try_worker_move(main, current_player['id'], valid_moves=valid_moves)
    if main._check_winner(current_player):
        print(f"{current_player['name']} wins!")
        break
    _clear_screen()
    print(main)
    valid_builds = main._valid_builds(current_player['id'])
    print(f"valid build:{valid_builds}")
    build = _try_build(main, current_player, valid_builds=valid_builds)
    # Advance Player Turn
    if not main._check_winnable():
        print("game is tied")
        break
    turn += 1
    current_player = player_list[turn%player_count]
    main._end_turn(current_player)

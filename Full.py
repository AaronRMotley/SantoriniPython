"""
Author: Aaron Motley
Santorini Text based or GUI game
"""

from itertools import groupby
from operator import itemgetter
from os import system, name


PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U", "V", "W",
          "X", "Y", "Z"]

# Game statistic trackers
no_winner, turn = True, 0


class BoardManager:
    """
    Create the board class and all local variables created for the game
    """
    def __init__(self, board_size=5, lvl_one_pcs=22, lvl_two_pcs=18, lvl_three_pcs=14, dome_pcs=18,
                 team=False, team_mod=2, player_count=2, enable_gods=False, worker_max=2, gui_enable=False):
        self.board_size = board_size
        self.lvl_one_pcs, self.lvl_two_pcs, self.lvl_three_pcs, self.dome_pcs = \
            lvl_one_pcs, lvl_two_pcs, lvl_three_pcs, dome_pcs
        self.team, self.team_mod, self.player_count, self.enable_gods = team, team_mod, player_count, enable_gods
        self.worker_max = worker_max
        self.gui_enable = gui_enable
        self.board = [[{'level': 0, 'dome': False, 'perimeter': False} for x in range(board_size)] for y in
                      range(board_size)]
        self.board_rework = [{'row': row, 'col': col, 'level': 0, 'dome': False, 'perimeter': False}
                             for row in range(board_size) for col in range(board_size)]
        for row_tuple in enumerate(self.board):
            for col_tuple in enumerate(self.board):
                if row_tuple[0] == 0 or row_tuple[0] == board_size - 1 \
                        or col_tuple[0] == 0 or col_tuple[0] == self.board_size - 1:
                    self.board[row_tuple[0]][col_tuple[0]]['perimeter'] = True

    def add_worker(self, player):
        number = len(self.player_pieces(player['id'])) + 1
        while True:
            row, col = self.input_to_coordinate(prompt="Select an empty row and column to place a worker: ")
            if 'worker' not in self.board[row][col]:
                self.board[row][col]['worker'] = {'moved': False, 'ascended': False, 'number': number, 'player': player}
                return True
            else:
                print(f'Worker already in space {row + 1},{col + 1}')
                continue



    def player_pieces(self, player_id):
        """given the player['id'] of a player
        return a list of board coordinates where that players workers are located

        In Team games return all team members pieces as well
        """
        pieces = []
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if 'worker' in col:
                    if col['worker']['player']['id'] == player_id \
                            or col['worker']['player']['id'] % self.team_mod == player_id % self.team_mod:
                        pieces.append([row_index, col_index])
        return pieces

    def valid_moves(self, player_id):
        """ Valid Moves returns a list containing [Origin_row, Origin_col, target_row, target_col,
            ] with numbers formatted for board rows and columns with values between 1 and 5
        """
        pieces = self.player_pieces(player_id)
        moves = []
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                if 'worker' in cell and [row_index, col_index] in pieces:
                    for target_row in range(row_index - 1, row_index + 2):
                        for target_col in range(col_index - 1, col_index + 2):
                            # Basic move without God attributes
                            if (
                                    self.board_size > target_row >= 0 and self.board_size > target_col >= 0
                                    and 'worker' not in self.board[target_row][target_col]
                                    and not self.board[target_row][target_col]['dome']
                                    # must not go up more than 1 level but can drop down to ground always
                                    and self.board[target_row][target_col]['level'] - 1 <=
                                    self.board[row_index][col_index][
                                        'level']
                            ):
                                moves.append([row_index, col_index, target_row, target_col])
        self._valid_moves_pretty_print(moves)
        return moves

    def move_worker(self, player_id, approved_moves=None):
        if not approved_moves:
            approved_moves = self.valid_moves(player_id)
        while True:
            try:
                if not approved_moves:
                    approved_moves = self.valid_moves(player_id)
                row, col = self.input_to_coordinate(prompt="Select a worker to move: ")
                requested_move = [row, col]
                if requested_move in self.player_pieces(player_id):
                    row, col = self.input_to_coordinate(prompt="Select a location to move to: ")
                    requested_move += [row, col]
                    print(requested_move)
                    if requested_move in approved_moves and len(requested_move) == 4:
                        self.board[requested_move[2]][requested_move[3]]['worker'] = \
                            self.board[requested_move[0]][requested_move[1]]['worker']
                        del (self.board[requested_move[0]][requested_move[1]]['worker'])
                        self.board[requested_move[2]][requested_move[3]]['worker']['moved'] = True
                        # if moved up a level: ascended == True
                        if self.board[requested_move[0]][requested_move[1]]['level'] < \
                                self.board[requested_move[2]][requested_move[3]]['level']:
                            self.board[requested_move[2]][requested_move[3]]['worker']['ascended'] = True
                        return True
                    else:
                        raise Exception("Not a valid move")
                else:
                    if 'worker' in self.board[requested_move[0]][requested_move[1]]:
                        raise Exception("Not your worker")
                    else:
                        raise Exception("No worker")
            except Exception as e:
                print(e)
                continue

    def valid_builds(self, player_id):
        """

        :param player_id:
        :return:
        """
        builds = []
        pieces = self.player_pieces(player_id)
        for row_index, row in enumerate(self.board):
            for col_index, cell in enumerate(row):
                if [row_index, col_index] in pieces and cell['worker']['moved']:
                    for target_row in range(row_index - 1, row_index + 2):
                        for target_col in range(col_index - 1, col_index + 2):
                            if (
                                    self.board_size > target_row >= 0 and 0 <= target_col < self.board_size
                                    and not (row_index == target_row and col_index == target_col)
                                    and not self.board[target_row][target_col]['dome']
                                    and 3 >= self.board[target_row][target_col]['level'] >= 0
                                    and 'worker' not in self.board[target_row][target_col]):
                                builds.append([target_row, target_col])
        return builds

    def build(self, player_id, approved_builds=None):
        if not approved_builds:
            approved_builds = self.valid_builds(player_id)
        while True:
            row, col = self.input_to_coordinate(prompt="Select a space to build: ")
            if [row, col] in approved_builds:
                if self.board[row][col]['level'] == 3:
                    self.board[row][col]['dome'] = True
                else:
                    self.board[row][col]['level'] += 1
                return True
            else:
                print(f"not a valid build spot {row + 1} {col + 1}")
                continue

    def end_turn(self, next_player_id):
        """

        :param next_player_id:
        """
        for r in self.board:
            for c in r:
                if 'worker' in c:
                    c['worker']['moved'] = False
                    if c['worker']['player']['id'] == next_player_id:
                        c['worker']['ascended'] = False

    def check_winner(self, player):
        """ check the board to see if a win condition as been done
        player is needed for special God rules, but not for vanilla game
        """
        if self.enable_gods:
            god = player['god']
            if god == 1:
                pass
                # TODO do god wins
        for r in self.board:
            for c in r:
                if 'worker' in c:
                    if c['level'] == 3:
                        return True
                    # TODO Or special God Win
        else:
            return False

    def check_winnable(self):
        """

        :return:
        """
        if self.lvl_three_pcs <= 0:
            for row in self.board:
                for cell in row:
                    if cell['level'] == 3 and not cell['dome']:
                        return True
            else:
                return False
        else:
            return True

    def __str__(self):
        s = (" " * (PRINT_SPACING + 1)).join(HEADER[:self.board_size + 1])
        for row_index, row in enumerate(self.board):
            s += '\n' + str(row_index + 1) + (" " * PRINT_SPACING)
            for cell in row:
                if cell['dome']:
                    s += "D^"
                else:
                    s += "L" + str(cell['level'])
                if 'worker' in cell:
                    s += "-" + str(cell['worker']['player']['color_name'][0]) + str(cell['worker']['number']) + (
                            " " * (PRINT_SPACING - 3))
                else:
                    s += (" " * PRINT_SPACING)
        return s + '\n'

    @staticmethod
    def _valid_moves_pretty_print(approved_builds=None):
        if not approved_builds:
            return False
        pretty_str = ''
        approved_builds = sorted(approved_builds, key=itemgetter(0, 1))
        grouped_moves = groupby(approved_builds, itemgetter(0, 1))
        for x in grouped_moves:
            pretty_str += str(x[0][0] + 1) + ',' + str(x[0][1] + 1) + ' ->'
            for y in x[1]:
                pretty_str += ' [' + str(y[2] + 1) + ',' + str(y[3] + 1) + '],'
            else:
                pretty_str = pretty_str[:-1]
                pretty_str += '\n'
        print(pretty_str)
        return True

    def input_to_coordinate(self, prompt='Enter comma separated coordinate (ex. a,2): '):
        """Asks for input to coordinate.
            If click_input if set to True, will wait for click and validate.
            If false, will ask for text input and validate. Will only accept values from 1 to max_board_size

            max_board_size default is 5
            click_input default is False

            Returns 2 values = Row, Col
        """
        if self.gui_enable:
            pass
            # TODO click input
        else:
            while True:
                try:
                    txt_list = input(f'{prompt}').split(',')
                    if len(txt_list) == 2:
                        coordinate = []
                        for txt in txt_list:
                            txt = ''.join(char for char in txt if char.isalnum())
                            coordinate.append(int(''.join([str(ord(char) - 96)
                                                           if char != '' and not char.isdigit()
                                                           else char for char in txt.lower()])))
                        for index, num in enumerate(coordinate):
                            if num < 1 or num > self.board_size:
                                raise Exception('value not on board')
                            else:
                                # Change coordinate from start 1 to start 0 for list management
                                coordinate[index] -= 1
                        else:
                            return coordinate[0], coordinate[1]
                    else:
                        raise Exception('Not valid entry. Example: a,1')
                except Exception as e:
                    print(e)
                    continue


#  End Main Board Object #

def create_player_list(is_gui=False):
    """

    :param is_gui:
    :return:
    """
    if is_gui:
        pass
    # TODO create ability to change player counts and player variables like color and gods
    player1 = {'id': 1, 'name': 'Player 1', 'hex_color': 'FF0000', 'god': '', 'color_name': 'Red'}
    player2 = {'id': 2, 'name': 'Player 2', 'hex_color': '0000FF', 'god': '', 'color_name': 'Blue'}
    # player3 = {'id':3,'name':'Player 3','hex_color':'008000','god':'','color_name':'Green'}
    compiled_list = [player1, player2]
    return compiled_list, len(compiled_list)


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
if __name__ == "__main__":
    try:
        main = BoardManager()
        player_list, players_in_game = create_player_list()

        players_placed = 0
        while players_placed < players_in_game:
            current_player = player_list[players_placed]
            work_count = 0
            while work_count < 2:
                print(main)
                print('\n' + current_player['name'])
                main.add_worker(current_player)
                _clear_screen()
                work_count += 1
            players_placed += 1

        # START GAME BASIC Terminal based
        current_player = player_list[0]
        while no_winner:
            _clear_screen()
            print(main)
            print(f"{current_player['name']} turn")
            if not main.move_worker(current_player['id']):
                raise Exception("failed to move worker")
            if main.check_winner(current_player):
                print(f"{current_player['name']} wins!")
                break
            _clear_screen()
            print(main)
            if not main.build(current_player):
                raise Exception("Failed to build")
            # Advance Player Turn
            if not main.check_winnable():
                print("game is tied")
                break
            turn += 1
            current_player = player_list[turn % players_in_game]
            main.end_turn(current_player)
    except Exception as e:
        print(e)
    finally:
        print("Bye")

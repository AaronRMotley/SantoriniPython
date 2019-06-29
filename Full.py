"""
Author: Aaron Motley
Santorini Text based or GUI board game
built in Python 3.7
"""

from itertools import groupby
from operator import itemgetter
from os import system, name

PRINT_SPACING = 5
HEADER = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U", "V", "W",
          "X", "Y", "Z"]


class BoardManager:
    """
    BoardManager class for Santorini board game runtime storage and logic methods
    Number of pieces, players, god enable, team enable, and other game options are customizable.
    Game logic is not. To change game logic you must edit the code and have an understanding of python3
    """

    def __init__(self, board_size=5, lvl_one_pcs=22, lvl_two_pcs=18, lvl_three_pcs=14, dome_pcs=18,
                 enable_team=False, player_count=2, enable_gods=False, worker_max=2, gui_enable=False):
        self.board_size = board_size
        self.worker_max = worker_max
        self.player_count = player_count
        self.lvl_one_pcs, self.lvl_two_pcs, self.lvl_three_pcs, self.dome_pcs = \
            lvl_one_pcs, lvl_two_pcs, lvl_three_pcs, dome_pcs
        self.enable_team = enable_team
        self.enable_gods = enable_gods
        self.gui_enable = gui_enable
        self.board = {(row, col): {'row': row, 'col': col, 'level': 0, 'dome': False}
                      for row in range(board_size) for col in range(board_size)}
        for (row, col), cell in self.board.items():
            if row == 0 or col == board_size - 1 \
                    or row == 0 or col == self.board_size - 1:
                cell['perimeter'] = True
            else:
                cell['perimeter'] = False

    # noinspection PyTypeChecker
    def add_worker(self, player):
        """
        Ask for input and place worker at selected coordinates

        :param player: Dict
        See create_player_list for player definition
        """
        number = len(self.player_pieces(player)) + 1
        placed = False
        while not placed:
            row_input, col_input = self.input_to_coordinate(prompt="Select an empty row and column to place a worker: ")
            for (row, col), cell in self.board.items():
                if row_input == row and col_input == col:
                    if 'worker' not in cell:
                        cell['worker'] = {'moved': False, 'ascended': False, 'number': number, 'player': player}
                        placed = True
                        break
                    else:
                        print(f'Worker already in space {row_input + 1},{col_input + 1}')
                        break

    def player_pieces(self, player):
        """
        :param player: Dict
        :return: list of lists where the worker's player_id is equal to the current player's id
        or if teams are enables, all pieces that share a team
        """
        pieces = []
        for (row, col), cell in self.board.items():
            if 'worker' in cell:
                if (cell['worker']['player']['id'] == player['id']
                        or (cell['worker']['player']['team'] == player['team'] and self.enable_team)):
                    pieces.append((row, col))
        return pieces

    def valid_moves(self, player):
        """
        :param player: Dict
        :return list of lists. inner list contains a 4 length list for [row, col, target_row, target_col]
        """
        pieces = self.player_pieces(player)
        validated_moves = []
        for (row, col), cell in self.board.items():
            if 'worker' in cell and (row, col) in pieces:
                for (target_row, target_col) in [(x, y) for x in range(row - 1, row + 2)
                                                 for y in range(col - 1, col + 2) if
                                                 not ((x == row and y == col) or not (
                                                         self.board_size > x >= 0 and self.board_size > y >= 0))]:
                    target_cell = self.board[(target_row, target_col)]
                    if ('worker' not in target_cell
                            and not target_cell['dome']
                            and target_cell['level'] - 1 <= cell['level']):
                        validated_moves.append((row, col, target_row, target_col))
        self._valid_moves_pretty_print(approved_moves=validated_moves)
        return validated_moves

    def move_worker(self, player):
        """
        :param player: Dict
        """
        approved_moves = self.valid_moves(player)
        if not approved_moves:
            return False
        origin_cell = {}
        while True:
            try:
                row, col = self.input_to_coordinate(prompt="Select a worker to move: ")
                target = (row, col)
                if target in self.player_pieces(player):
                    row, col = self.input_to_coordinate(prompt="Select a location to move to: ")
                    target += (row, col)
                    if target in approved_moves and len(target) == 4:
                        origin_cell = self.board[(target[0], target[1])]
                        target_cell = self.board[(target[2], target[3])]
                        target_cell['worker'] = origin_cell['worker']
                        del (origin_cell['worker'])
                        target_cell['worker']['moved'] = True
                        # if moved up a level: ascended == True
                        if origin_cell['level'] < target_cell['level']:
                            target_cell['worker']['ascended'] = True
                        return True
                    else:
                        raise Exception("Not a valid move")
                else:
                    if 'worker' in origin_cell:
                        raise Exception("Not your worker")
                    else:
                        raise Exception("No worker")
            except Exception as e:
                print(e)
                continue

    def valid_builds(self, player):
        """
        :param player: Dict
        :return: list of lists. inner list contains a 4 length list for [row, col, target_row, target_col]
        """
        builds = []
        pieces = self.player_pieces(player)
        for (row, col), cell in self.board.items():
            if (row, col) in pieces and cell['worker']['moved']:
                for (target_row, target_col) in [(x, y) for x in range(row - 1, row + 2)
                                                 for y in range(col - 1, col + 2) if
                                                 not ((x == row and y == col) or not (
                                                         self.board_size > x >= 0 and self.board_size > y >= 0))]:
                    target_cell = self.board[(target_row, target_col)]
                    if (self.board_size > target_cell['row'] >= 0 and 0 <= target_cell['col'] < self.board_size
                            and not target_cell['dome'] and 'worker' not in target_cell
                            and not (target_cell['level'] == 0 and self.lvl_one_pcs <= 0)
                            and not (target_cell['level'] == 1 and self.lvl_two_pcs <= 0)
                            and not (target_cell['level'] == 2 and self.lvl_three_pcs <= 0)
                            and not (target_cell['level'] == 3 and self.dome_pcs <= 0)):
                        builds.append((target_row, target_col))
        return builds

    def build(self, player):
        """

        :param player:
        :return:
        """
        approved_builds = self.valid_builds(player)
        print(approved_builds)
        if not approved_builds:
            print("no valid builds")
            return False
        while True:
            try:
                row, col = self.input_to_coordinate(prompt="Select a space to build: ")
                if (row, col) in approved_builds:
                    build_cell = self.board[(row, col)]
                    if build_cell['level'] == 3:
                        build_cell['dome'] = True
                        self.dome_pcs -= 1
                    elif build_cell['level'] == 2:
                        build_cell['level'] = 3
                        self.lvl_three_pcs -= 1
                    elif build_cell['level'] == 1:
                        build_cell['level'] = 2
                        self.lvl_two_pcs -= 1
                    elif build_cell['level'] == 0:
                        build_cell['level'] = 1
                        self.lvl_two_pcs -= 1
                    else:
                        raise Exception("current level not found")
                    return True
                else:
                    raise Exception(f"not a valid build spot {row + 1} {col + 1}")
            except Exception as e:
                print(e)
                continue

    def end_turn(self, player):
        """

        :param player:
        """
        for cell in self.board.values():
            if 'worker' in cell and (cell['worker']['player']['id'] == player['id']
                                     or (cell['worker']['player']['team'] == player['team'] and self.enable_team)):
                cell['worker']['moved'] = False
                cell['worker']['ascended'] = False

    def check_winner(self, player):
        """ check the board to see if a win condition as been done
        player is needed for special God rules, but not for vanilla game
        """
        if self.enable_gods:
            god = player['god']
            if god:
                pass
            # TODO do god wins
        for cell in self.board.values():
            if 'worker' in cell:
                if cell['level'] == 3:
                    return True
                # TODO Or special God Win
        else:
            return False

    def check_winnable(self):
        """

        :return:
        """
        if self.lvl_three_pcs <= 0:
            for cell in self.board.values():
                if cell['level'] == 3 and not cell['dome']:
                    return True
            else:
                return False
        else:
            return True

    def __str__(self):
        s = (" " * (PRINT_SPACING + 1)).join(HEADER[:self.board_size + 1])
        current_row = -1
        for (row, col), cell in self.board.items():
            if current_row != row:
                s += '\n' + str(row + 1) + (" " * PRINT_SPACING)
                current_row = row
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
    def _valid_moves_pretty_print(approved_moves=None):
        if approved_moves:
            pretty_str = ''
            approved_moves = sorted(approved_moves, key=itemgetter(0, 1))
            grouped_moves = groupby(approved_moves, key=itemgetter(0, 1))
            for x in grouped_moves:
                pretty_str += str(x[0][0] + 1) + ',' + str(x[0][1] + 1) + ' ->'
                for y in x[1]:
                    pretty_str += ' [' + str(y[2] + 1) + ',' + str(y[3] + 1) + '],'
                else:
                    pretty_str = pretty_str[:-1]
                    pretty_str += '\n'
            print(pretty_str)

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
    player1 = {'id': 1, 'name': 'Player 1', 'hex_color': 'FF0000', 'god': '', 'color_name': 'Red', 'team': 1}
    player2 = {'id': 2, 'name': 'Player 2', 'hex_color': '0000FF', 'god': '', 'color_name': 'Blue', 'team': 2}
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
        turn = 0
        player_list, players_in_game = create_player_list()
        main = BoardManager(player_count=players_in_game)
        players_placed = 0
        while players_placed < main.player_count:
            current_player = player_list[players_placed]
            work_count = 0
            while work_count < main.worker_max:
                print(main)
                print('\n' + current_player['name'])
                main.add_worker(current_player)
                _clear_screen()
                work_count += 1
            players_placed += 1

        # START GAME BASIC Terminal based
        current_player = player_list[0]
        while True:
            _clear_screen()
            print(main)
            print(f"{current_player['name']} turn")
            if not main.move_worker(current_player):
                print("failed to move worker")
            if main.check_winner(current_player):
                print(f"{current_player['name']} wins!")
                break
            _clear_screen()
            print(main)
            if not main.build(current_player):
                print("Failed to build")
            # Advance Player Turn
            if not main.check_winnable():
                print("game is tied- no winner")
                break
            turn += 1
            current_player = player_list[turn % main.player_count]
            main.end_turn(current_player)
    except Exception as fail_message:
        print(fail_message)
    finally:
        print("Bye")

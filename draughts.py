from PIL import Image  # from pillow
import copy


class Player:
    def __init__(self, name, nb):
        self.name = name
        self.nb = nb
        self.eat_move_queen = list()
        self.eat_move_pieces = list()
        self.nb_pieces = 20
        self.color = None
        self.get_color()

    def clear_moves(self):
        self.eat_move_queen = list()
        self.eat_move_pieces = list()

    def get_color(self):
        if self.nb == -1:
            self.color = "white"
        elif self.nb == 1:
            self.color = "black"


def generate_grid(board):
    pionNN_img = Image.open("src_draughts/pionNN.png")
    pionNR_img = Image.open("src_draughts/pionNR.png")
    pionBN_img = Image.open("src_draughts/pionBN.png")
    pionBR_img = Image.open("src_draughts/pionBR.png")
    dict_pieces = {1: pionNN_img, 2: pionNR_img, -1: pionBN_img, -2: pionBR_img}
    boardIMG = Image.open("src_draughts/draughtboard.png")
    for row_index, row in enumerate(board):
        for column_index, piece in enumerate(row):
            if piece == 0:
                continue
            else:
                boardIMG.paste(dict_pieces[piece],
                               (column_index * 50 + 50, row_index * 50 + 50),
                               dict_pieces[piece])

    boardIMG.save("src_draughts/images/current_draughtboard.png")


def update(board, msg):
    generate_grid(board)
    print(msg)


def valid_move(move, turn, board, players_list):
    move = move.split(" ")
    grid_index = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}

    def select_indexes(_column: str, _row: int, what: str):

        if what == "initial" and _column in grid_index:
            return _row - 1, grid_index[_column]
        elif what == "final" and _column in grid_index:
            return _row - 1, grid_index[_column]
        else:
            return None

    def check_valid_2(place, what: str):
        if isinstance(place[0], str) and isinstance(place[1], int):
            return select_indexes(place[0], int(place[1]), what)
        elif isinstance(place[0], int) and isinstance(place[1], str):
            return select_indexes(place[1], int(place[0]), what)

    def check_valid_3(place, what: str):

        # du type A10
        if isinstance(place[0], str) and isinstance(place[1], int) and isinstance(place[2], int):
            if 1 <= int(str(place[1]) + str(place[2])) <= 10:
                return select_indexes(place[0], int(str(place[1]) + str(place[2])), what)
            else:
                return None

        # du type 10A celui ci qu ilag
        elif isinstance(place[0], int) and isinstance(place[1], int) and isinstance(place[2], str):
            if 1 <= int(place[0] + place[1]) <= 10:
                return select_indexes(place[2], int(str(place[0]) + str(place[1])), what)
            else:
                return None

        else:
            return None

    if len(move) == 2:

        # row: str ; column : int
        valid_moves = True
        row_Init = None
        column_Init = None
        row_Final = None
        column_Final = None
        initial_place = list(move[0])
        move_place = list(move[1])

        for index, mv in enumerate(initial_place):
            try:
                initial_place[index] = int(mv)
            except ValueError:
                initial_place[index] = mv.upper()

        for index, mv in enumerate(move_place):
            try:
                move_place[index] = int(mv)
            except ValueError:
                move_place[index] = mv.upper()

        # initial coords the number has a len of 1
        if len(initial_place) == 2:
            result = check_valid_2(initial_place, "initial")
            if result is None:
                valid_moves = False
            else:
                row_Init, column_Init = result

        # initial coords the number has a len of 2
        elif len(initial_place) == 3:
            result = check_valid_3(initial_place, 'initial')
            if result is None:
                valid_moves = False
            else:
                row_Init, column_Init = result
        else:
            valid_moves = False

        # final coords the number has a len of 1
        if len(move_place) == 2:
            result = check_valid_2(move_place, 'final')
            if result is None:
                valid_moves = False
            else:
                row_Final, column_Final = result

        # initial coords the number has a len of 2
        elif len(move_place) == 3:
            result = check_valid_3(move_place, 'final')
            if result is None:
                valid_moves = False
            else:
                row_Final, column_Final = result
        else:
            valid_moves = False

        if valid_moves:
            if board[row_Init][column_Init] == turn[0]:

                # normal white piece, it has to go up
                if turn[0] == -1 and row_Init == row_Final + 1 and (
                        column_Init == column_Final + 1 or column_Init == column_Final - 1):

                    return verify_move(column_Init, row_Init, column_Final, row_Final, True, "piece", turn, board,
                                       players_list)

                # normal black piece, it has to go down
                elif turn[0] == 1 and row_Init == row_Final - 1 and (
                        column_Init == column_Final + 1 or column_Init == column_Final - 1):

                    return verify_move(column_Init, row_Init, column_Final, row_Final, True, "piece", turn, board,
                                       players_list)

                # other moves
                else:
                    return verify_move(column_Init, row_Init, column_Final, row_Final, False, "piece", turn, board,
                                       players_list)

            # queen
            elif board[row_Init][column_Init] == turn[0] * 2:

                # normal move for a queen
                if abs(abs(row_Init) - abs(row_Final)) == abs(abs(column_Init) - abs(column_Final)):

                    # verify if there are pieces between the initial move and the final
                    has_to_eat = False
                    a, b = row_Init, column_Init
                    row_diff = row_Final - row_Init
                    col_diff = column_Final - column_Init
                    while row_Final != a:
                        if board[a][b] == turn[0] * -1:
                            has_to_eat = True
                            break
                        a += int(row_diff / abs(row_diff))
                        b += int(col_diff / abs(col_diff))

                    return verify_move(column_Init, row_Init, column_Final, row_Final, not has_to_eat, "queen", turn,
                                       board,
                                       players_list)
                else:
                    return verify_move(column_Init, row_Init, column_Final, row_Final, False, "queen", turn, board,
                                       players_list)

            else:
                pass


def have_force_move(member_nb: int, player: Player, board):
    def check_can_eat_pieces(rInit, cInit, mv_id: list, root: list):
        initial_root = copy.deepcopy(root)

        for ID_coo, coords in enumerate(mv_id):
            # vérifier si les coordonnées ne sont pas fausses
            if 0 <= 2 * coords[0] + rInit <= 9 and 0 <= 2 * coords[1] + cInit <= 9:

                # Les 2 pions suivants sont celui de l'autre joueur ou que ce soit un de ses pions
                if (board[coords[0] + rInit][coords[1] + cInit] == -member_nb or
                    board[coords[0] + rInit][coords[1] + cInit] == member_nb * -2) and \
                        (board[2 * coords[0] + rInit][2 * coords[1] + cInit] == -member_nb or
                         board[2 * coords[0] + rInit][2 * coords[1] + cInit] == -member_nb * 2) or \
                        (board[coords[0] + rInit][coords[1] + cInit] == member_nb or
                         board[coords[0] + rInit][coords[1] + cInit] == 2 * member_nb):
                    continue

                # le point de départ est ce celui du joueur est celui d'arrivée n'est pas occupé
                if (board[coords[0] + rInit][coords[1] + cInit] == member_nb * -1 or
                    board[coords[0] + rInit][coords[1] + cInit] == member_nb * -2) and \
                        board[2 * coords[0] + rInit][2 * coords[1] + cInit] == 0:

                    # voir si le point a déjà été mangé
                    def pion_eaten():
                        if len(root) != 0:
                            for pion_dict in root:
                                if pion_dict['pos_piece_eaten'] == [coords[0] + rInit, coords[1] + cInit]:
                                    return True
                            return False
                        else:
                            return False

                    if not pion_eaten():

                        root.append({"pos_piece": [rInit, cInit],
                                     "pos_piece_eaten": [coords[0] + rInit, coords[1] + cInit],
                                     "piece_arriving": [2 * coords[0] + rInit, 2 * coords[1] + cInit]})

                        # supprimer le sens qui vient d'être fait
                        mvs_id = copy.deepcopy(index_list)
                        for w_id, w in enumerate(mvs_id):
                            if w[0] * -1 == coords[0] and w[1] * -1 == coords[1]:
                                del mvs_id[w_id]
                                break

                        check_can_eat_pieces(2 * coords[0] + rInit, 2 * coords[1] + cInit, mvs_id, root=root)

                        if len(root) != 0:
                            piece_list.append(root)

                        root = copy.deepcopy(initial_root)

    def check_can_eat_queen(rInit, cInit, mv_id: list, root: list):

        for ID_coo, coords in enumerate(mv_id):
            a, b = coords[0], coords[1]
            while True:

                # vérifier si les coordonnées ne sont pas fausses (ne sortent pas du damier)
                if 0 <= a + rInit + coords[0] <= 9 and 0 <= b + cInit + coords[1] <= 9:

                    # Les 2 emplacements qui suivent sont des pions ou qu'il voir qu'il y a un pion à lui
                    if (abs(board[a + rInit][b + cInit]) == 1 or
                        abs(board[a + rInit][b + cInit]) == 2) and \
                            (abs(board[a + rInit + coords[0]][b + cInit + coords[1]]) == 1 or
                             abs(board[a + rInit + coords[0]][b + cInit + coords[1]]) == 2) or \
                            board[a + rInit][b + cInit] == member_nb or \
                            board[a + rInit][b + cInit] == member_nb * 2:
                        break

                    # vérifier le pion est celui de l'adversaire et que celui d'après est vide
                    if (board[a + rInit][b + cInit] == member_nb * -1 or
                        board[a + rInit][b + cInit] == member_nb * -2) and \
                            board[a + rInit + coords[0]][b + cInit + coords[1]] == 0:

                        # voir si le point a déjà été mangé
                        pion_eaten = False
                        if len(root) != 0:
                            for pion_dict in root:
                                if pion_dict['pos_piece'] == [a + rInit, b + cInit]:
                                    pion_eaten = True
                                    break

                        if not pion_eaten:

                            if len(root) == 0:
                                if not rInit == row_id and not cInit == column_id:
                                    a += coords[0]
                                    b += coords[1]
                                    continue

                            root.append({"pos_queen": [rInit, cInit], "pos_piece": [a + rInit, b + cInit]})

                            while True:

                                a += coords[0]
                                b += coords[1]

                                # correspond à la case derrière le pion qui est vide (vérifié plus tôt)
                                if not 0 <= a + rInit <= 9 or not 0 <= b + cInit <= 9 or \
                                        board[a + rInit][b + cInit] == (
                                        abs(member_nb) or abs(member_nb * 2)):
                                    break
                                else:

                                    # supprimer le sens qui vient d'être fait
                                    mvs_id = copy.deepcopy(index_list)
                                    for w_id, w in enumerate(mvs_id):
                                        if w[0] * -1 == coords[0] and w[1] * -1 == coords[1]:
                                            del mvs_id[w_id]
                                            break

                                    check_can_eat_queen(a + rInit, b + cInit, mvs_id, root=root)

                            if not root in queen_list:
                                queen_list.append(root)

                            root = []

                        else:
                            a += coords[0]
                            b += coords[1]
                            continue

                else:
                    break

                a += coords[0]
                b += coords[1]

    player.clear_moves()
    index_list = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
    queen_list = []
    piece_list = []

    # lister tous les pions de la grille
    for row_id, row in enumerate(board):
        for column_id, column in enumerate(row):

            # c'est un pion normal
            if column == member_nb:
                check_can_eat_pieces(rInit=row_id, cInit=column_id, mv_id=index_list, root=[])

            # c'est une dame
            elif column == member_nb * 2:
                check_can_eat_queen(rInit=row_id, cInit=column_id, mv_id=index_list, root=[])

    player.eat_move_queen = queen_list
    for item in piece_list:
        if not item in player.eat_move_pieces:
            player.eat_move_pieces.append(item)


def set_move(column_Init: int, row_Init: int, column_Final: int, row_Final: int,
             what: str, delete_pieces: list, turn, board, player, players_list):
    other_player = players_list[players_list.index(player) - 1]

    if len(delete_pieces) > 0:
        for coords in delete_pieces:
            board[coords[0]][coords[1]] = 0
        other_player.nb_pieces -= len(delete_pieces)

    board[row_Init][column_Init] = 0

    if what == 'piece':
        board[row_Final][column_Final] = turn[0]
        check_transform_queen(row_Final, column_Final, turn[0], board)
    elif what == "queen":
        board[row_Final][column_Final] = turn[0] * 2

    return True


def check_transform_queen(row: int, col: int, player_nb, board):
    if row == 0 and player_nb == -1:
        board[row][col] = -2
    elif row == len(board) - 1 and player_nb == 1:
        board[row][col] = 2


def verify_move(column_Init: int, row_Init: int, column_Final: int, row_Final: int,
                checked: bool, what: str, turn, board, players_list):
    player = turn[1]
    # modify list eat_moves et eat_moves_queen
    have_force_move(turn[0], player, board)

    # no forced moves
    if len(player.eat_move_queen) == 0 and len(player.eat_move_pieces) == 0:

        if board[row_Final][column_Final] == 0 and checked and what == "piece":
            return set_move(column_Init, row_Init, column_Final, row_Final, what, [], turn, board, player, players_list)

        if board[row_Final][column_Final] == 0 and checked and what == "queen":
            return set_move(column_Init, row_Init, column_Final, row_Final, what, [], turn, board, player, players_list)

    # has forced move(s)
    else:
        final_choice, greatest_nb = list(), 0
        right_choice_list = []
        delete_pieces_list = []

        # trier tous les mouvements les plus longs
        for LM_id, long_moves in enumerate(player.eat_move_pieces):
            if len(long_moves) == greatest_nb:
                final_choice.append(long_moves)
            elif len(long_moves) > greatest_nb:
                greatest_nb = len(long_moves)
                final_choice.clear()
                final_choice.append(long_moves)

        for LM_id, long_moves in enumerate(player.eat_move_queen):
            if len(long_moves) == greatest_nb:
                final_choice.append(long_moves)
            elif len(long_moves) > greatest_nb:
                greatest_nb = len(long_moves)
                final_choice.clear()
                final_choice.append(long_moves)

        for LM_id, long_moves in enumerate(final_choice):

            if "pos_queen" in long_moves[0] and what == "queen":
                if long_moves[0]["pos_queen"] == [row_Init, column_Init]:
                    coef_coords = [long_moves[-1]['pos_piece'][0] - long_moves[-1]['pos_queen'][0],
                                   long_moves[-1]['pos_piece'][1] - long_moves[-1]['pos_queen'][1]]
                    coef_coords = [int(coef_coords[0] / abs(coef_coords[0])),
                                   int(coef_coords[1] / abs(coef_coords[1]))]
                    a = coef_coords[0]
                    b = coef_coords[1]

                    # vérifier le mouvement final
                    while True:

                        # vérifier si les coordonnées ne sortent pas du damier
                        if 0 <= long_moves[-1]['pos_queen'][0] + a <= 9 and 0 <= long_moves[-1]['pos_queen'][
                            1] + b <= 9:

                            # vérifier si la piont final est dans la diagonale du pion mangé et l'emplacement de la dame
                            if row_Final == long_moves[-1]['pos_queen'][0] + a and column_Final == \
                                    long_moves[-1]['pos_queen'][1] + b:
                                right_choice_list.append(long_moves)
                                break
                        else:
                            break

                        a += coef_coords[0]
                        b += coef_coords[1]

            elif "piece_arriving" in long_moves[0] and what == "piece":
                if long_moves[0]["pos_piece"] != [row_Init, column_Init] or long_moves[-1]["piece_arriving"] != [
                    row_Final, column_Final]:
                    continue
                right_choice_list.append(long_moves)

        if len(right_choice_list) == 0:
            return False
        else:
            if what == "piece":
                for long_move in right_choice_list:
                    for coords in long_move:
                        delete_pieces_list.append(coords["pos_piece_eaten"])
                    break

                return set_move(column_Init, row_Init, column_Final, row_Final, what, delete_pieces_list, turn, board,
                                player, players_list)

            elif what == "queen":
                for long_move in right_choice_list:
                    for coords in long_move:
                        delete_pieces_list.append(coords["pos_piece"])
                    break

                return set_move(column_Init, row_Init, column_Final, row_Final, what, delete_pieces_list, turn, board,
                                player, players_list)


def check_victory(turn, players_list):
    player, other_player = turn[1], players_list[players_list.index(turn[1]) - 1]
    if other_player.nb_pieces != 0:
        turn[0] *= -1
        turn[1] = other_player
        return False

    # player has won
    else:
        return player


# -1 = white
# 1 = black
original_draughts_grid = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                          [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                          [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
                          [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                          [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0]]

_draughts_grid = copy.deepcopy(original_draughts_grid)
_turn = [-1, None]
# list of Player
_players_list = []

for i in range(2):

    # if the name already used
    while True:
        same = False
        name = str(input(f"{i + 1} player, what would be your username ?"))
        for _player in _players_list:
            if name == _player.name:
                same = True

        if not same:
            break
        print("This username is already used")

    # first player
    if i == 0:
        while True:
            begin = str(input(f"{name}, do you want to begin ? yes / no "))
            if begin == "yes":
                _players_list.append(Player(name, -1))
                _turn[1] = _players_list[0]
                break
            elif begin == "no":
                _players_list.append(Player(name, 1))
                break

    # second player
    else:
        if _turn[1] is None:
            _players_list.append(Player(name, -1))
            _turn[1] = _players_list[-1]
        else:
            _players_list.append(Player(name, 1))

print("\n-------------\n"
      "Open the image \"current_draughtboard.png\"\n"
      "-------------\n")

update(_draughts_grid, f"{_turn[1].name}, you have to begin, you are {_turn[1].color}")
# the game begins
while True:
    _move = str(input("Type your move : "))
    if not valid_move(_move, _turn, _draughts_grid, _players_list):
        print("Invalid move")
        continue
    won = check_victory(_turn, _players_list)
    if not won:
        update(_draughts_grid, f"{_turn[1].name}, it is your turn to play, you are {_turn[1].color}")
        continue
    else:
        update(_draughts_grid, f"Congratulatiosn, you won {won.name} !!")
        break

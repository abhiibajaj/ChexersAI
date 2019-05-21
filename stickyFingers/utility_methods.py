import copy


def find_moves(piece, player_colour, board, pure_board):
    """
    All valid moves by a piece given a board state.
    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y)
    * `board` -- a dictionary of { piece : player } representing the board state
    * `player` -- player is the String colour, ie. "red"
    """
    moves = []
    # see where we can exit
    if is_exit(piece, player_colour):
        exit_move = ("EXIT", piece)
        moves.append(exit_move)

    # see where we can jump
    moves += jump_moves(piece, board, pure_board)

    # see where we can move normally
    moves += regular_moves(piece, board, pure_board)
    return moves


def jumped_coord(action):
    """
    Given an action, return the coordinates that were jumped over

    Arguments:
    * `action` -- a 2 tuple of coordinates (src, dest)
    """
    # do maths
    # get player coord we jumped over
    src = action[1][0]
    dst = action[1][1]

    xdir = dst[0] - src[0]
    ydir = dst[1] - src[1]

    jumpedx = src[0] + piece_sign(xdir)
    jumpedy = src[1] + piece_sign(ydir)

    return (jumpedx, jumpedy)


def piece_sign(pdir):
    """
    return the sign of a number

    Arguments:
    * `pdir` -- integer
    """
    if pdir == 0:
        return 0
    elif pdir > 0:
        return 1
    else:
        return -1


def jump_moves(piece, board, pure_board):
    """
    Find all valid jump moves a piece can make given a board state.
    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y)
    * `board` -- a dictionary of { piece : player } representing the board state
        where player is a String color, ie "red"
    """
    regular_moves = radial_moves(piece, 1)
    jump_moves = radial_moves(piece, 2)

    valid_moves = []
    # filter out invalid moves
    # for surrounding move spaces
    for (index, regular_move) in enumerate(regular_moves, 0):
        # if there is someone to jump over
        if regular_move in board:
            # the position of the jump
            jump_move = jump_moves[index]
            # if the jump position is not occupied
            if jump_move not in board:
                # if the jump is a space on the board
                if jump_move in pure_board:
                    # turn the move into a move tuple
                    valid_move = ("JUMP", (piece, jump_move))
                    valid_moves.append(valid_move)

    return valid_moves


def regular_moves(piece, board, pure_board):
    """
    Find all valid regular moves a piece can make given a board state.
    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y)
    * `board` -- a dictionary of { piece : player } representing the board state
        where player is a String color, ie "red"
    """
    moves = radial_moves(piece, 1)
    valid_moves = []

    # filter out invalid moves
    for move in moves:
        # if it is not occupied
        if move not in board:
            # if the move exists
            if move in pure_board:
                # turn the move into a move tuple
                valid_move = ("MOVE", (piece, move))
                valid_moves.append(valid_move)

    return valid_moves


def radial_moves(piece, radius):
    """
    Helper function to find all radial moves outward from a center coordinate.
    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y), taken as the center.
    * `radius` -- the range of the radius outwards,
        ie. radius 1 = a regular move
        radius 2 = a jump move
    """

    east = (piece[0] + radius, piece[1])
    west = (piece[0] - radius, piece[1])
    northwest = (piece[0], piece[1] - radius)
    northeast = (piece[0] + radius, piece[1] - radius)
    southwest = (piece[0] - radius, piece[1] + radius)
    southeast = (piece[0], piece[1] + radius)

    return [east, west, northeast, northwest, southeast, southwest]


def is_exit(piece, player_colour):
    """
    Given a piece coordinate, return if a given player can exit

    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y)
    * `player` -- player is the String colour, ie. "red"
    """
    if player_colour == "red":
        return (piece in player_exits("red"))
    if player_colour == "green":
        return (piece in player_exits("green"))
    if player_colour == "blue":
        return (piece in player_exits("blue"))


def close_by_friends(piece, player_colour, board):
    """
    Helper function that returns the friendly pieces that a given piece
    is neighbouring

    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y), taken as the center.
    * `player_colour` -- string enum, "red", "green", "blue"
    * `board` -- a set of pieces that represent a board
    """

    # return friendly pieces that you are close to
    friendly_pieces = 0
    possible_radials = radial_moves(piece, 1)

    for radial in possible_radials:
        # check if the radial is the same colour as you
        try:
            collision_piece = board[radial]
            if collision_piece == player_colour:
                friendly_pieces += 1
        except KeyError:
            pass
    return friendly_pieces


def can_be_captured(piece, player_colour, board, pure_board):
    """
    Helper function that returns if a piece can be captured

    Arguments:
    * `piece` -- a 2 tuple of coordinates (x, y), taken as the center.
    * `player_colour` -- string enum, "red", "green", "blue"
    * `board` -- a set of pieces that represent a board
    * `pure_board` -- all the piece coords on a board
    """
    possible_radials = radial_moves(piece, 1)
    for radial in possible_radials:

        try:
            collision_piece = board[radial]
            # check if can be captured by seeing if anyone can actually jump
            # over it
            if collision_piece != player_colour:

                # check the jump moves for the collision piece
                jump_radials = jump_moves(radial, board, pure_board)
                for jump in jump_radials:
                    # if you jump over the piece, return false
                    if jumped_coord(jump) == piece:
                        # print('{} can be captured by {}'.format(piece, radial))
                        return True
        except KeyError:
            pass
    return False


def player_exits(player_colour):
    """
    Return the exits for a given piece colour
    Arguments:
    * `player_colour` -- string enum, "red", "green", "blue"
    """
    if player_colour == "red":
        return [(3, -3), (3, -2), (3, -1), (3, 0)]
    elif player_colour == "green":
        return [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
    elif player_colour == "blue":
        return [(-3, 0), (-2, -1), (-1, -2), (0, -3)]
    else:
        return []


def weighted_total_score(score_list, weight_list):
    """
    Apply multiplication index wise between two lists
    of values

    Arguments:
    * `score_list` -- array of array of values
    * `weight_list` -- array of array ofvalues
    """
    score_total = [0, 0, 0]
    for pair_score, pair_weight in zip(score_list, weight_list):
        weighted_scored = list(map(lambda x: pair_weight*x, pair_score))

        for i in range(len(score_total)):
            score_total[i] += weighted_scored[i]
    return score_total


def get_player_id(player_colour):
    """
    Get the id of a player

    Arguments:
    * `player_colour` -- string enum, "red", "green", "blue"
    """
    if player_colour == 'red':
        return 0
    elif player_colour == 'green':
        return 1
    elif player_colour == 'blue':
        return 2


def get_player_pieces(player_colour, board_info):
    """
    Get the pieces of a given player

    Arguments:
    * `player_colour` -- string enum of colours
    * `board_info` -- a Board() instance
    """
    player_pieces = set()

    for piece_coord, piece_colour in board_info.board.items():
        if piece_colour == player_colour:
            player_pieces.add(piece_coord)

    return player_pieces


def get_next_colour(player_colour, board_info):
    """
    Get the player_colour that is after the given player_colour's turn

    Arguments:
    * `player_colour` -- string enum of colours
    * `board_info` -- a Board() instance
    """
    # choose the next player
    if player_colour == 'red':
        next_colour = 'green'
    elif player_colour == 'green':
        next_colour = 'blue'
    elif player_colour == 'blue':
        next_colour = 'red'

    # check if the player we are handing over to still has pieces
    for _, colour in board_info.board.items():
        # next_colour still has a piece
        if next_colour == colour:
            return next_colour

    # recursively find the next player
    return get_next_colour(next_colour, board_info)


def manhattan_dist(a, b):
    """
    Get the player_colour that is after the given player_colour's turn

    Arguments:
    * `a` -- coord, (x, y)
    * `b` -- coord, (x, y)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def sort_moves(move):
    move_type, _ = move
    if move_type == "EXIT":
        return 1
    elif move_type == "JUMP":
        return 2
    else:
        return 3

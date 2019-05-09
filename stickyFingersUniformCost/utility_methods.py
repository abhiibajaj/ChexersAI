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
    jump_moves    = radial_moves(piece, 2)

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
    moves       = radial_moves(piece, 1)
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
        
    east      = (piece[0] + radius, piece[1])
    west      = (piece[0] - radius, piece[1])
    northwest = (piece[0]         , piece[1] - radius)
    northeast = (piece[0] + radius, piece[1] - radius)
    southwest = (piece[0] - radius, piece[1] + radius)
    southeast = (piece[0]         , piece[1] + radius)

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

# all exits for each color
def player_exits(player_colour):
    """
    Return the exits for a given piece colour
    Arguments:
    * `player_colour` -- a String, ie. "red"
    """
    if player_colour == "red":
        return [(3, -3), (3, -2), (3, -1), (3, 0)]
    elif player_colour == "green":
        return [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
    elif player_colour == "blue":
        return [(-3, 0), (-2, -1), (-1, -2), (0, -3)]
    else:
        return []

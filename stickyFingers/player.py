
from board import *

class Player:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (Red, Green or Blue). The value will be one of the 
        strings "red", "green", or "blue" correspondingly.
        """
        # TODO: Set up state representation.
        self.boardInfo = Board()

        self.colour = colour

        self.pieces = self.boardInfo.player_starts(colour)
        self.exits = self.boardInfo.player_exits(colour)


        self.update(colour, ("MOVE", ((-3, 0), (-2, 0))))
        self.boardInfo.print_board()


    

    def is_exit(chex):
        """
        Given a chex coordinate, return if a given player can exit
        Arguments:
        * `chex` -- a 2 tuple of coordinates (x, y)
        * `player` -- player is the String colour, ie. "red"
        """
        return chex in self.exits
        
    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        """
        # TODO: Decide what action to take.
        return ("PASS", None)

    def radial_moves(self, piece, radius):
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

    def regular_moves(piece):
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
            if move not in self.boardInfo.board:
                # if the move exists
                if move in self.boardInfo.pure_board:
                    # turn the move into a move tuple
                    valid_move = (piece, move, "MOVE")
                    valid_moves.append(valid_move)

        return valid_moves
        
    def jump_moves(piece):
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
            if regular_move in self.boardInfo.board:
                # the position of the jump
                jump_move = jump_moves[index]
                # if the jump position is not occupied
                if jump_move not in self.boardInfo.board:
                    # if the jump is a space on the board
                    if jump_move in self.boardInfo.pure_board:
                        # turn the move into a move tuple
                        valid_move = (piece, jump_move, "JUMP")
                        valid_moves.append(valid_move)

        return valid_moves

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red", 
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or 
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action 
        (or pass) for the player colour (your method does not need to validate 
        the action/pass against the game rules).
        """
        # TODO: Update state representation in response to action.


        self.boardInfo.update_board(colour, action)

player = Player('red')
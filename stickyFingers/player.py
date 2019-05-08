
from board import *
import sys
import heapq
from maxn import *

class ExamplePlayer:
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
        self.board_info = Board()

        self.colour = colour

        self.pieces = self.board_info.player_starts(colour)
        self.exits = self.board_info.player_exits(colour)

        self.maxn_strat = MaxN(self, self.board_info)

        # self.update(colour, ("MOVE", ((-3, 0), (-2, 0))))
        # self.board_info.print_board(debug=True)        
    

    def is_exit(self, piece):
        """
        Given a chex coordinate, return if a given player can exit
        Arguments:
        * `piece` -- a 2 tuple of coordinates (x, y)
        """
        return piece in self.exits
        
    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. If there are no allowed 
        actions, your player must return a pass instead. The action (or pass) 
        must be represented based on the above instructions for representing 
        actions.
        # TODO: Decide what action to take.

        for piece in self.pieces:
            path = self.uniform_cost_search(piece)
            action = path[0]
            break
        self.update_pieces(action)
        return action
        """

        (score, action_to_take) = self.maxn_strat.max_n(3, self.board_info.player_id[self.colour])
        print(action_to_take)

    def uniform_cost_search(self, piece):
        """
        A uniform cost search algorithm for finding an exit for a given piece

        Arguments:
        * `piece` -- a 2 tuple of coordinates (x, y)
        * `board` -- a dictionary of { piece : player } representing the board state
        * `player` -- player is the String colour, ie. "red"
        """
        openSet = []
        heapq.heapify(openSet)

        closedSet = {}
        closedSet[piece] = None

        # push starting piece into open set
        # (heauristic + steps, steps, the piece)
        value = (0, 0, piece)
        heapq.heappush(openSet, value)

        while openSet:
            steps, _, the_piece = heapq.heappop(openSet)

            if self.is_exit(the_piece):            
                # reconstruct the path that got us to the exit
                return self.reconstruct_path(the_piece, closedSet)

            # find the moves this piece can make
            my_moves = self.find_moves(the_piece)
            
            # for each move
            for move in my_moves:
                steps_inc = steps + 1
                _, dest, move_type = move
                distance_from_goal = steps_inc
                # see if it goes anywhere new
                if dest not in closedSet.keys():
                    # it does, add it to the heap
                    closedSet[dest] = (move_type, (the_piece, dest))
                    heapq.heappush(openSet, (steps_inc, distance_from_goal, dest))
        return ("PASS", None)


    def reconstruct_path(self, curr_coord, seen_moves):
        """
        Reconstruct a path from a uniform cost seach dictionary `seen_moves`
        """
        path = [ ( "EXIT", curr_coord) ]
        while seen_moves[curr_coord] != None:

            path.append(seen_moves[curr_coord])
            curr_coord = seen_moves[curr_coord][1][0]
        # reverse it, so it goes start to end
        return path[::-1]

    def update_pieces(self, action):
        
        action_type = action[0]
        action_coords = action[1]

        if action_type == "PASS":
            pass
        
        elif action_type == "EXIT":
            self.pieces.remove(action_coords)
        else:
            src = action_coords[0]
            dest = action_coords[1]

            self.pieces.remove(src)
            self.pieces.add(dest)
                        # see if we jumped over another colour
            if action_type == "JUMP":
                jumped = self.jumped_coord(action)
                # if we did, change its colour
                self.pieces.add(jumped)
                
    def jumped_coord(self, action):
        # do maths
        # get player coord we jumped over
        src = action[1][0]
        dst = action[1][1]

        xdir = dst[0] - src[0]
        ydir = dst[1] - src[1]

        jumpedx = src[0] + self.piece_sign(xdir)
        jumpedy = src[1] + self.piece_sign(ydir)

        return (jumpedx, jumpedy)

    def piece_sign(self, pdir):
        if pdir == 0:
            return 0
        elif pdir > 0:
            return 1
        else:
            return -1


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

    def regular_moves(self, piece):
        """
        Find all valid regular moves a piece can make given a board state.
        Arguments:
        * `piece` -- a 2 tuple of coordinates (x, y)
        * `board` -- a dictionary of { piece : player } representing the board state
            where player is a String color, ie "red"
        """
        moves       = self.radial_moves(piece, 1)
        valid_moves = []

        # filter out invalid moves
        for move in moves:
            # if it is not occupied
            if move not in self.board_info.board:
                # if the move exists
                if move in self.board_info.pure_board:
                    # turn the move into a move tuple
                    valid_move = (piece, move, "MOVE")
                    valid_moves.append(valid_move)

        return valid_moves
        
    def jump_moves(self, piece):
        """
        Find all valid jump moves a piece can make given a board state.
        Arguments:
        * `piece` -- a 2 tuple of coordinates (x, y)
        * `board` -- a dictionary of { piece : player } representing the board state
            where player is a String color, ie "red"
        """
        regular_moves = self.radial_moves(piece, 1)
        jump_moves    = self.radial_moves(piece, 2)

        valid_moves = []
        # filter out invalid moves
        # for surrounding move spaces
        for (index, regular_move) in enumerate(regular_moves, 0):
            # if there is someone to jump over
            if regular_move in self.board_info.board:
                # the position of the jump
                jump_move = jump_moves[index]
                # if the jump position is not occupied
                if jump_move not in self.board_info.board:
                    # if the jump is a space on the board
                    if jump_move in self.board_info.pure_board:
                        # turn the move into a move tuple
                        valid_move = (piece, jump_move, "JUMP")
                        valid_moves.append(valid_move)

        return valid_moves


    def find_moves(self, piece):
        """
        All valid moves by a piece given a board state.
        Arguments:
        * `piece` -- a 2 tuple of coordinates (x, y)
        * `board` -- a dictionary of { piece : player } representing the board state
        * `player` -- player is the String colour, ie. "red"
        """
        moves = []
        # see where we can exit
        if self.is_exit(piece):
            exit_move = (piece, piece, "EXIT")
            moves.append(exit_move)

        # see where we can jump
        moves += self.jump_moves(piece)

        # see where we can move normally
        moves += self.regular_moves(piece)
        return moves

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

        # print(self.board_info.board)

        self.board_info.update_board(colour, action)

        to_remove = set()
        #if action[0] == "JUMP":
        
        for piece in self.pieces:
            if self.board_info.board[piece] != self.colour:
               

                to_remove.add(piece)
        
        # Make this a func
        for remove_coords in to_remove:
            self.pieces.remove(remove_coords)

player = ExamplePlayer('red')
player.action()

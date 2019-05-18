
from stickyFingers.board import *
import sys
import heapq
from stickyFingers.maxn import *
from stickyFingers.minimax import *
from stickyFingers.openingstrat import *
from stickyFingers.uniform_cost import *
from stickyFingers.utility_methods import *
from collections import defaultdict


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
        self.board_info = Board()

        self.colour = colour

        self.pieces = self.board_info.player_starts(colour)
        # self.exits = self.board_info.player_exits(colour)
        self.opening_flag = True
        self.maxn_flag = False
        self.minimax_flag = False

        self.opening_strat = OpeningStrategy(self, self.board_info)
        self.maxn_strat = MaxN("Jump")
        self.minimax_strat = Minimax("Jump")
        self.uniform_cost_strat = UniformCostSearch()
        self.moves_made = 0
        # self.update(colour, ("MOVE", ((-3, 0), (-2, 0))))
        # self.board_info.print_board(debug=True)

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
        """

        num_pieces = defaultdict(int)
        for piece, piece_colour in self.board_info.board.items():
            num_pieces[piece_colour] += 1

        # make opening moves until done
        if self.opening_flag:
            # print("OPENING")
            action_to_take = self.opening_strat.move()
            if action_to_take is None:
                self.opening_flag = False
                self.maxn_flag = True

        if len(num_pieces) == 1:
            self.maxn_flag = False
            self.minimax_flag = False

        elif len(num_pieces) == 2:
            self.maxn_flag = False
            self.minimax_flag = True

        if self.maxn_flag:
            # print("NOT OPENING")
            (score, action_to_take) = self.maxn_strat.max_n(3, self.colour,
                                                            self.board_info,
                                                            self.colour)
            # print((score, action_to_take))
        elif self.minimax_flag:
            (score, action_to_take) = self.minimax_strat.alphabeta(
                4, self.colour, self.colour, self.board_info, float('-inf'), float('inf'), True)
        elif self.opening_flag is False and self.maxn_flag is False and self.minimax_flag is False:
            action_to_take = self.uniform_cost_strat.uniform_action(
                self.pieces, self.colour, self.board_info.board,
                self.board_info.pure_board
            )

        self.moves_made += 1
        self.update_pieces(action_to_take)

        return action_to_take

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
                jumped = jumped_coord(action)
                # if we did, change its colour
                self.pieces.add(jumped)

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

        # TODO Make this a func
        # handle when a piece is converted by the move we just made
        to_remove = set()
        # for each of our pieces
        for piece in self.pieces:
            # if it has been taken by an opponent
            if self.board_info.board[piece] != self.colour:
                # mark it for removal
                to_remove.add(piece)

        # remove it from our available pieces
        for remove_coords in to_remove:
            self.pieces.remove(remove_coords)


# player0 = Player('red')
# player1 = Player('green')
# player2 = Player('blue')
# action  = player0.action()

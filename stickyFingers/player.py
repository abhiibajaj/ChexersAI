
from stickyFingers.board import *
import sys
import heapq
from stickyFingers.maxn import *
from stickyFingers.uniform_cost import *
from stickyFingers.utility_methods import *


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
        # self.exits = self.board_info.player_exits(colour)
        
        self.maxn_strat = MaxN(self.board_info)
        self.uniform_cost_strat = UniformCostSearch()

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

        

        # (score, action_to_take) = self.maxn_strat.max_n(3, self.colour, 
        #                                                 self.board_info,
        #                                                 self.colour)

        action_to_take = self.uniform_cost_strat.uniform_action(
            self.pieces, self.colour, self.board_info.board,
            self.board_info.pure_board
        )
        # if action_to_take[0] == "EXIT":
        #     action_to_take = ("EXIT", (action_to_take[1][0]))
        # print("FINL SCORE FOR RED: ", score)
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

        to_remove = set()
        # if action[0] == "JUMP":
        
        for piece in self.pieces:
            if self.board_info.board[piece] != self.colour:
               

                to_remove.add(piece)
        
        # Make this a func
        for remove_coords in to_remove:
            self.pieces.remove(remove_coords)

player0 = ExamplePlayer('red')
# player0.action()
# print(player0.find_moves((3,0)))
player1 = ExamplePlayer('green')
player2 = ExamplePlayer('blue')
action  = player0.action()
player0.update(player0.colour, action)
player1.update(player0.colour, action)
player2.update(player0.colour, action)
# player0.board_info.print_board()
# player1.action()
# player2.action()


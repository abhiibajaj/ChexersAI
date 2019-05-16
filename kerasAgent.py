from chexersWrapper import chexersWrapper
from stickyFingers.utility_methods import *
from stickyFingers.board import *
from stickyFingers.uniform_cost import *

pure_board = Board().get_pure_board()
ucs = UniformCostSearch()
game = chexersWrapper()


def handle_gameover(player):
    print("Game winner", player)


def handle_turn(player, state):
    print("State: ", state)

    my_pieces = set()
    for piece, colour in state.items():
        if colour == player:
            my_pieces.add(piece)

    action_to_take = ucs.uniform_action(
        my_pieces, player, state,
        pure_board
    )
    print(action_to_take)
    return action_to_take


game.run(handle_gameover, handle_turn)

import copy
from math import sqrt
from stickyFingers.utility_methods import *
from stickyFingers.heuristic_abstract import *


class Minimax:

    def __init__(self, strategy):
        self.strategy = Heurisitic(strategy)

    def is_terminal_board(self, board_info):
        # check that a player is 1 move away from winning
        terminal = False

        # check if the new board state is terminal zz
        for score in board_info.scores.values():
            terminal = terminal or (score == 4)

        return terminal

    def alphabeta(self, depth, player_colour, prev_colour, board_info, alpha, beta, maximizing_player):

        best_a = ('PASS', None)

        if depth == 0 or self.is_terminal_board(board_info):
            evaluation = (self.strategy.score(
                player_colour, board_info, prev_colour, True), best_a)
            return evaluation

        if maximizing_player:
            value = float('-inf')

            player_pieces = get_player_pieces(player_colour, board_info)
            for piece in player_pieces:
                all_moves = find_moves(piece, player_colour, board_info.board,
                                       board_info.pure_board)
                for move in all_moves:

                    board_info_copy = copy.deepcopy(board_info)
                    board_info_copy.update_board(player_colour, move)

                    next_player = get_next_colour(
                        player_colour, board_info_copy)

                    (new_value, action) = self.alphabeta(
                        depth-1, next_player, player_colour, board_info_copy, alpha, beta, False)
                    print('{} score for {}, colour {}'.format(
                        new_value, move, player_colour))
                    if new_value > value:
                        value = new_value
                        best_a = move
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        # print('prune')
                        break
                if alpha >= beta:
                    break
            # print(str(player_colour) + " max picked " +
            #       str(best_a) + " score was : " + str(value))
            return (value, best_a)
        else:

            value = float('inf')
            player_pieces = get_player_pieces(player_colour, board_info)
            for piece in player_pieces:
                all_moves = find_moves(piece, player_colour, board_info.board,
                                       board_info.pure_board)

                for move in all_moves:
                    board_info_copy = copy.deepcopy(board_info)
                    board_info_copy.update_board(player_colour, move)

                    next_player = get_next_colour(
                        player_colour, board_info_copy)

                    (new_value, action) = self.alphabeta(
                        depth-1, next_player, player_colour, board_info_copy, alpha, beta, True)

                    print('{} score for {}, colour {}'.format(
                        new_value, move, player_colour))
                    if new_value < value:
                        value = new_value
                        best_a = move
                    beta = min(beta, value)
                    if alpha >= beta:
                        # print('prune')

                        break
                if alpha >= beta:
                    break
            # print(str(player_colour) + " min picked " +
            #       str(best_a) + " score was : " + str(value))
            return (value, best_a)

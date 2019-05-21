import copy
from math import sqrt
from stickyFingers.utility_methods import *
from stickyFingers.heuristic_abstract import *


class MaxN:

    def __init__(self, strategy):
        self.strategy = Heurisitic(strategy)

    def is_terminal_board(self, board_info):
        """
        Check if a board has a winner
        """
        # check that a player is 1 move away from winning
        terminal = False

        # check if the new board state is terminal zz
        for score in board_info.scores.values():
            terminal = terminal or (score == 4)

        return terminal

    def max_n(self, depth, player_colour, board_info, prev_colour, curr=0):
        """
        MaxN algorithm
        Prioritise game states where we win and avoid game states where we lose
        """
        # Default action
        best_a = ("PASS", None)

        # base case or max depth reached
        if depth == 0 or self.is_terminal_board(board_info):
            evaluation = (self.strategy.score(prev_colour, board_info), best_a)
            return evaluation

        vmax = (float('-inf'), float('-inf'), float('-inf'))
        player_pieces = self.get_player_pieces(player_colour, board_info)

        # for each piece this player has
        for piece in player_pieces:
            all_moves = find_moves(piece, player_colour, board_info.board,
                                   board_info.pure_board)

            # for each move this piece can make
            for move in all_moves:
                safe_to_make = True
                if safe_to_make:
                    # evaluate the worth of this move
                    board_info_copy = copy.deepcopy(board_info)
                    board_info_copy.update_board(player_colour, move)

                    next_player = self.get_next_colour(
                        player_colour, board_info_copy)

                    (score, _) = self.max_n(depth - 1, next_player,
                                            board_info_copy, player_colour, curr+1)

                    player_id = get_player_id(player_colour)

                    # store the best move this player can make
                    if score[player_id] > vmax[player_id]:
                        vmax = score
                        best_a = move

                    # Do somrthing here, minimise everyone else
                    elif score[player_id] == vmax[player_id]:
                        score_other = sum(score)
                        score_vmax_other = sum(vmax)

                        if score_other < score_vmax_other:
                            vmax = score
                            best_a = move

                    if float('inf') in vmax:
                        return (vmax, best_a)

                else:
                    pass
            # Immediately prune
            if float('inf') in vmax:
                break

        return (vmax, best_a)

    def safe_move(self, move, player_colour, board_info):
        """
        Check for collisions and capture states
        """
        if move[0] == 'EXIT':
            return True

        piece = move[1][1]
        safe_to_make = True
        possible_radials = radial_moves(piece, 1)

        board_info_copy = copy.deepcopy(board_info)
        board_info_copy.update_board(player_colour, move)
        if can_be_captured(piece, player_colour, board_info_copy.board, board_info_copy.pure_board):
            return False
        return True

    def get_player_pieces(self, player_colour, board_info):
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

    def get_next_colour(self, player_colour, board_info):
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
        return self.get_next_colour(next_colour, board_info)

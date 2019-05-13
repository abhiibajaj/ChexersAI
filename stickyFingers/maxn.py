import copy
from math import sqrt
from stickyFingers.utility_methods import *


class MaxN:

    def __init__(self, board_info):
        self.board_info = board_info

    def is_terminal_board(self):
        # check that a player is 1 move away from winning
        terminal = False

        for score in self.board_info.scores.values():
            terminal = terminal or (score == 4)

        return terminal

    def heuristic(self, player_colour, board_info):
        score = [0, 0, 0]
        player_id = self.get_player_id(player_colour)
        score[player_id] += board_info.scores[player_colour]

        # if we can jump, good
        # if we can jump over an enemy, good good
        # if we can be jumped by an enemy, bad
        # if we are closer to the exit, goodish?

        min_dist = float('inf')
        max_dist = 100
        # for each piece on the board
        for piece, piece_colour in board_info.board.items():
            # if we are close to the exit, good
            exits = player_exits(piece_colour)
            player_id = self.get_player_id(piece_colour)

            # find the closest exit
            for player_exit in exits:
                min_dist = min(
                    min_dist, self.manhattan_dist(piece, player_exit))

            # normalise the score
            score[player_id] += (max_dist - min_dist) / max_dist

        return score

    def manhattan_dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def max_n(self, depth, player_colour, board_info, prev_colour, curr=0):
        # Default action
        best_a = ("PASS", None)

        # base case or max depth reached
        if depth == 0 or self.is_terminal_board():
            evaluation = (self.heuristic(prev_colour, board_info), best_a)
            return evaluation

        vmax = (float('-inf'), float('-inf'), float('-inf'))
        player_pieces = self.get_player_pieces(player_colour, board_info)

        # for each piece this player has
        for piece in player_pieces:
            all_moves = find_moves(piece, player_colour, board_info.board,
                                   board_info.pure_board)
            # for each move this piece can make
            for move in all_moves:
                # evaluate the worth of this move
                board_info_copy = copy.deepcopy(board_info)
                board_info_copy.update_board(player_colour, move)

                next_player = self.get_next_colour(
                    player_colour, board_info_copy)

                (score, _) = self.max_n(depth - 1, next_player,
                                        board_info_copy, player_colour, curr+1)

                player_id = self.get_player_id(player_colour)

                # store the best move this player can make
                if score[player_id] > vmax[player_id]:
                    vmax = score
                    best_a = move
            break

        print(str(player_colour) + " picked " +
              str(best_a) + " score was : " + str(vmax))
        # board_info.print_board(debug=True)

        return (vmax, best_a)

    def get_player_pieces(self, player_colour, board_info):
        player_pieces = set()

        for piece_coord, piece_colour in board_info.board.items():
            if piece_colour == player_colour:
                player_pieces.add(piece_coord)

        return player_pieces

    def get_player_id(self, player_colour):
        if player_colour == 'red':
            return 0
        elif player_colour == 'green':
            return 1
        elif player_colour == 'blue':
            return 2

    def get_next_colour(self, player_colour, board_info):
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

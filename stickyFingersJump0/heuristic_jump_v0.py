from stickyFingersJump0.utility_methods import *
from collections import defaultdict


class HeuristicJump0:
    def score(self, player_colour, board_info):

        score = [0, 0, 0]
        player_id = get_player_id(player_colour)

        num_pieces = defaultdict(int)
        for piece, piece_colour in board_info.board.items():
            num_pieces[piece_colour] += 1

        for piece_colour, pieces_count in num_pieces.items():

            player_id = get_player_id(piece_colour)
            score[player_id] += pieces_count

        return score

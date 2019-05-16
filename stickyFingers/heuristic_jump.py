from stickyFingers.utility_methods import *
from collections import defaultdict


class HeuristicJump:
    def score(self, player_colour, board_info):

        score = [0, 0, 0]
        player_id = get_player_id(player_colour)

        num_pieces = defaultdict(int)

        # Account for how many pieces have made it through
        for piece_colour, piece_score in board_info.scores.items():
            player_id = get_player_id(piece_colour)
            # If score is higher than 4 then piece colour will win
            if piece_score >= 4:
                score[player_id] = float('inf')
            else:
                score[player_id] = piece_score

        for piece, piece_colour in board_info.board.items():
            player_id = get_player_id(piece_colour)
            # get how many friendly pieces you have touching
            friendly_pieces = close_by_friends(
                piece, piece_colour, board_info.board)
            score[player_id] += 0.1 * friendly_pieces

        for piece, piece_colour in board_info.board.items():
            num_pieces[piece_colour] += 1
        for piece_colour, pieces_count in num_pieces.items():

            player_id = get_player_id(piece_colour)
            score[player_id] += 5*pieces_count

            # for piece_colour_copy, pieces_count_copy in num_pieces.items():

            #     if piece_colour != piece_colour_copy:

            #         score[player_id] -= pieces_count_copy

        return score

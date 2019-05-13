from stickyFingers.utility_methods import *
from collections import defaultdict

class HeuristicJump0:
    def score(self, player_colour, board_info):

        score = [0, 0, 0]
        player_id = get_player_id(player_colour)

        num_pieces = defaultdict(int)
        for piece, piece_colour in board_info.board.items():
            num_pieces[piece_colour] += 1

        # for piece_colour, piece_score in board_info.scores.items():
        #     player_id = get_player_id(piece_colour)
        #     score[player_id] += piece_score

        for piece_colour, pieces_count in num_pieces.items():

            player_id = get_player_id(piece_colour)
            score[player_id] += pieces_count

            # for piece_colour_copy, pieces_count_copy in num_pieces.items():

            #     if piece_colour != piece_colour_copy:

            #         score[player_id] -= pieces_count_copy


        # for piece, piece_colour in board_info.board.items():
        #     player_id = get_player_id(piece_colour)

        #     # if piece can be captured -1
        #     possible_radials = radial_moves(piece, 1)
        #     for move in possible_radials:
        #         if move in board_info.pure_board:
        #             try:
        #                 collision_piece = board_info.board[move]
        #                 if collision_piece != piece_colour:
        #                     score[player_id] -= 1
        #                     break
        #             except KeyError:
        #                 pass

        return score
    


                


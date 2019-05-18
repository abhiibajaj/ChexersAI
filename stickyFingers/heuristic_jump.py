from stickyFingers.utility_methods import *
from stickyFingers.uniform_cost import *
from collections import defaultdict


class HeuristicJump:
    def __init__(self):
        self.uniform_cost_strat = UniformCostSearch()

    def score(self, player_colour, board_info, minimax=False):

        score_total = [0, 0, 0]

        score_manhat = [0, 0, 0]
        score_friends = [0, 0, 0]
        score_points = [0, 0, 0]
        score_threatned = [0, 0, 0]
        score_pieces_alive = [0, 0, 0]

        # Get how many pieces each player has
        num_pieces = defaultdict(int)
        for piece, piece_colour in board_info.board.items():
            num_pieces[piece_colour] += 1

        # Weight it by the manhattan distance: THIS WORKS BETTER/FASTER THAN PATH
        for piece, piece_colour in board_info.board.items():
            # if we are close to the exit, good
            exits = player_exits(piece_colour)
            player_id = get_player_id(piece_colour)

            min_dist = float('inf')
            # find the closest exit
            for player_exit in exits:
                min_dist = min(
                    min_dist,  manhattan_dist(piece, player_exit))

            score_manhat[player_id] -= (
                (1 / num_pieces[piece_colour]) * min_dist)

        # Account for how many pieces have made it through
        for piece_colour, piece_score in board_info.scores.items():
            player_id = get_player_id(piece_colour)
            # If score is higher than 4 then piece colour will win
            if piece_score >= 4:
                score_points[player_id] = float('inf')

            else:
                score_points[player_id] = piece_score

        # Weight how many friends you have: POWER IN NUMBERS !
        for piece, piece_colour in board_info.board.items():
            player_id = get_player_id(piece_colour)
            # get how many friendly pieces you have touching
            friendly_pieces = close_by_friends(
                piece, piece_colour, board_info.board)
            score_friends[player_id] += friendly_pieces

        # Minus how many pieces can be capture
        for piece, piece_colour in board_info.board.items():
            player_id = get_player_id(piece_colour)
            if can_be_captured(piece, piece_colour, board_info.board, board_info.pure_board):
                score_threatned[player_id] -= 1

        # Maximise the pieces you have
        for piece_colour, pieces_count in num_pieces.items():

            player_id = get_player_id(piece_colour)
            score_pieces_alive[player_id] += pieces_count

        # Weights for each metric
        w_manhat = 0.15
        w_friends = 0.05

        w_threatned = 1

        w_points = 1
        w_points_close = 10

        w_pieces_alive_close = 0
        w_pieces_alive = 5

        w_pieces_percent = 0.60

        # if you have over 60% of pieces look to exit
        total_pieces = sum([x for x in num_pieces.values()])
        for piece_colour, piece_count in num_pieces.items():
            if (piece_count + board_info.scores[piece_colour] * 1.0) / total_pieces > w_pieces_percent:
                # print("HERE FOR ", piece_colour)
                player_id = get_player_id(piece_colour)
                if board_info.scores[piece_colour] + piece_count >= 4:
                    score_manhat[player_id] *= 2
                    score_points[player_id] *= 500
                    score_threatned[player_id] *= 10
                    # score_pieces_alive[player_id] *= 0.8

        score_list = [
            score_manhat,
            score_friends,
            score_points,
            score_threatned,
            score_pieces_alive,
        ]

        weight_list = [
            w_manhat,
            w_friends,
            w_points,
            w_threatned,
            w_pieces_alive,
        ]

        score_total = weighted_total_score(score_list, weight_list)
        if minimax:

            player_id = get_player_id(player_colour)
            # print(score_total[player_id])
            return score_total[player_id]
        return score_total

from stickyFingers.utility_methods import *
from stickyFingers.uniform_cost import *
from collections import defaultdict


class HeuristicJump:
    def __init__(self):
        self.uniform_cost_strat = UniformCostSearch()

    def score(self, player_colour, board_info, prev_colour=None, minimax=False):
        """
        A heuristic that pays attention to

        - manhatten distance to the exit
        - how many friends a piece has
        - how many points a player has
        - how many pieces are threatened
        - how many pieces are alive

        Then apply weights to each, fine tuned by hand.
        """
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

        manhat_maps = defaultdict(int)
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

            # count how many close pieces we have
            if min_dist > -2:
                manhat_maps[player_colour] += 1

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
            if can_be_captured(piece, piece_colour, board_info.board,
                               board_info.pure_board):
                score_threatned[player_id] -= 1

        # Maximise the pieces you have
        for piece_colour, pieces_count in num_pieces.items():

            player_id = get_player_id(piece_colour)
            # add pieces we have
            score_pieces_alive[player_id] += pieces_count
            # add our score
            score_pieces_alive[player_id] += score_points[player_id]

        # Weights for each metric
        w_manhat = 0.15
        w_friends = 0.05
        w_threatned = 1

        w_points = 1
        w_points_close = 1

        w_pieces_alive_close = 0
        w_pieces_alive = 5

        w_pieces_percent = 0.50

        # try to capture if someone else is winning
        for piece_colour, piece_count in num_pieces.items():
            goalie_flag = False

            player_id = get_player_id(piece_colour)
            for other_colour, other_count in num_pieces.items():
                if piece_colour != other_colour:
                    other_id = get_player_id(other_colour)

                    # Other player can win and has many pieces close to the exit
                    if (other_count + board_info.scores[other_colour]) >= 4 \
                            and score_manhat[other_id] <= 0 \
                            and score_manhat[other_id] >= -3:
                        player_new_manhat = self.manhat_exits(
                            board_info.board, piece_colour,
                            player_exits(other_colour), num_pieces
                        )
                        goalie_flag = True
                        score_manhat[player_id] = player_new_manhat * 3

                        break
            # If no one else is close to winning, try get the player to win
            if goalie_flag is False:

                piece_close_count = manhat_maps[piece_colour]
                if (piece_close_count + board_info.scores[piece_colour] >= 4):

                    score_manhat[player_id] *= 5
                    score_points[player_id] *= 500

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
            return score_total[player_id]
        return score_total

    def manhat_exits(self, board, player_colour, other_exits, num_pieces):

        score_goal_manhat = 0
        min_dist = float('inf')
        for piece, piece_colour in board.items():
            if piece_colour == player_colour:

                for other_exit in other_exits:
                    min_dist = min(
                        min_dist,  manhattan_dist(piece, other_exit))

            score_goal_manhat -= (
                (1 / num_pieces[piece_colour]) * min_dist)
        return score_goal_manhat

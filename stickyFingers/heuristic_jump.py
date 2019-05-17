from stickyFingers.utility_methods import *
from stickyFingers.uniform_cost import *
from collections import defaultdict


class HeuristicJump:
    def __init__(self):
        self.uniform_cost_strat = UniformCostSearch()

    def score(self, player_colour, board_info):

        score = [0, 0, 0]

        # Weight the distance from the goal

        # THIS IS IF YOU DO IT WITH UNIFORM COST, TAKES WAY TOO LONG
        # for piece, piece_colour in board_info.board.items():
        #     player_id = get_player_id(piece_colour)
        #     # Get the path for the current piece and subtract it from the score
        #     path = self.uniform_cost_strat.uniform_cost_search(
        #         piece, piece_colour, board_info.board, board_info.pure_board)
        #     score[player_id] -= len(path)

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

            score[player_id] = ((1 / num_pieces[piece_colour]) * min_dist)

        # Account for how many pieces have made it through
        for piece_colour, piece_score in board_info.scores.items():
            player_id = get_player_id(piece_colour)
            # If score is higher than 4 then piece colour will win
            if piece_score >= 4:
                score[player_id] = float('inf')
            else:
                score[player_id] = piece_score

        # Weight how many friends you have: POWER IN NUMBERS !
        for piece, piece_colour in board_info.board.items():
            player_id = get_player_id(piece_colour)
            # get how many friendly pieces you have touching
            friendly_pieces = close_by_friends(
                piece, piece_colour, board_info.board)
            score[player_id] += 0.01 * friendly_pieces

        # Minus how many pieces can be capture
        for piece, piece_colour in board_info.board.items():
            player_id = get_player_id(piece_colour)
            if can_be_captured(piece, player_colour, board_info.board, board_info.pure_board):
                score[player_id] -= 1

        # Maximise the pieces you have
        for piece_colour, pieces_count in num_pieces.items():

            player_id = get_player_id(piece_colour)
            score[player_id] += pieces_count

        return score

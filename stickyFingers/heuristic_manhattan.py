# Come back to this
class HeurisiticManhattan:
    def __init__(self):
        print("HI")
        
    def score(self, player_colour, board_info):
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
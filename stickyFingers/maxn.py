class MaxN:
    def __init__(self, player, board_info):
        self.board_info = board_info
        self.player = player

    def is_terminal_board(self):
        # check that a player is 1 move away from winning
        terminal = False

        for score in self.board_info.scores.values():
            terminal = terminal or (score == 4)

        return terminal

    def heuristic(self):
        return (1, 1, 1)

    def make_possible_board_states(self):
        return []

    def max_n(self, depth, player_id):
        best_a = ("PASS", None)
        if depth == 0 or self.is_terminal_board():
            return (self.heuristic(), best_a)

        vmax = (float('-inf'), float('-inf'), float('-inf'))

        for piece in self.player.pieces:
            all_moves = self.player.find_moves(piece)
            for move in all_moves:
                if player_id + 1 > 2:
                    player_id = 0
                (score, _) = self.max_n(depth - 1, player_id + 1)
                if score[player_id] > vmax[player_id]:
                    vmax = score
                    best_a = (move[2], (move[0], move[1]))

        return (vmax, best_a)

import copy
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

    def max_n(self, depth, player_colour, board_info):


        # Default action
        best_a = ("PASS", None)

        if depth == 0 or self.is_terminal_board():
            return (self.heuristic(), best_a)


        vmax = (float('-inf'), float('-inf'), float('-inf'))

        for piece in self.player.pieces:
            # proper formatting 
            all_moves = self.player.find_moves(piece)

            for move in all_moves:
                board_info_copy = copy.deepcopy(board_info)
                

                proper_move = (move[2], (move[0], move[1]))

                board_info_copy.update_board(player_colour, proper_move)
                # print(board_info.board)
                # print(board_info_copy.board)

                (score, _) = self.max_n(depth - 1, 
                                        self.get_next_colour(player_colour),
                                        board_info_copy)
                player_id = self.get_player_id(player_colour)
                if score[player_id] > vmax[player_id]:
                    vmax = score
                    best_a = (move[2], (move[0], move[1]))
        print(best_a)
        return (vmax, best_a)

    def get_player_id(self, player_colour):
        if player_colour == 'red':
            return 0
        elif player_colour == 'green':
            return 1
        else:
            return 2

    def get_next_colour(self, player_colour):

        if player_colour == 'red':
            return 'green'
        elif player_colour == 'green':
            return 'blue'
        else:
            return 'red'
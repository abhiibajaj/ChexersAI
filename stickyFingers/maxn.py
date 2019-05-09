import copy
from math import sqrt

class MaxN:
       
    def __init__(self, player, board_info):
        self.player = player
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

        # player_pieces = self.get_player_pieces(player_colour, board_info)

        
        min_dist = float('inf')
        for piece, piece_colour in board_info.board.items():
            player_exits = board_info.player_exits(piece_colour)
            player_id = self.get_player_id(piece_colour)

            for player_exit in player_exits:
                min_dist = min(min_dist, self.calc_square_dist(piece, player_exit))
                # print(min_dist)
                # calc t,
            # min dist between all pieces?
            score[player_id] -= min_dist
        print("SCORE: ", score)

        return score

    def calc_square_dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def max_n(self, depth, player_colour, board_info):


        # Default action
        best_a = ("PASS", None)

        if depth == 0 or self.is_terminal_board():
            return (self.heuristic(player_colour, board_info), best_a)


        vmax = (float('-inf'), float('-inf'), float('-inf'))
        player_pieces = self.get_player_pieces(player_colour, board_info)

        for piece in player_pieces:
            # proper formatting 
            all_moves = self.player.find_moves(piece)

            for move in all_moves:
                board_info_copy = copy.deepcopy(board_info)
                

                proper_move = (move[2], (move[0], move[1]))
                if move[2] == "EXIT":
                    proper_move = (move[2], (move[0]))
                board_info_copy.update_board(player_colour, proper_move)

                (score, _) = self.max_n(depth - 1, 
                                        self.get_next_colour(player_colour),
                                        board_info_copy)
                player_id = self.get_player_id(player_colour)
                if score[player_id] > vmax[player_id]:
                    vmax = score
                    best_a = (move[2], (move[0], move[1]))
            break
        
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
        else:
            return 2

    def get_next_colour(self, player_colour):

        if player_colour == 'red':
            return 'green'
        elif player_colour == 'green':
            return 'blue'
        else:
            return 'red'
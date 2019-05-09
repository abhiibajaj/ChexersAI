import copy
from math import sqrt
from stickyFingers.utility_methods import *

class MaxN:
       
    def __init__(self, board_info):
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
            exits = player_exits(piece_colour)
            player_id = self.get_player_id(piece_colour)

            for player_exit in exits:
                min_dist = min(min_dist, self.calc_square_dist(piece, player_exit))
                # print(min_dist)
                # calc t,
            # min dist between all pieces?
            score[player_id] -= min_dist
        # board_info.print_board(debug=True)
        print("PLayer colour for score ", player_colour)

        print("SCORE: ", score)

        print()
        print()
 

        return score

    def calc_square_dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def max_n(self, depth, player_colour, board_info, prev_colour,curr=0):


        # Default action
        best_a = ("PASS", None)

        if depth == 0 or self.is_terminal_board():
            evaluation = (self.heuristic(prev_colour, board_info), best_a)
            return evaluation


        vmax = (float('-inf'), float('-inf'), float('-inf'))
        player_pieces = self.get_player_pieces(player_colour, board_info)

        print("Current move: " + str(curr) + " for " + str(player_colour))
        for piece in player_pieces:
            # proper formatting 
            all_moves = find_moves(piece, player_colour, board_info.board, 
                                    board_info.pure_board)
            for move in all_moves:
                board_info_copy = copy.deepcopy(board_info)
                

                
                board_info_copy.update_board(player_colour, move)
                # board_info_copy.print_board()

                (score, _) = self.max_n(depth - 1, 
                                        self.get_next_colour(player_colour),
                                        board_info_copy, player_colour, curr+1)
                player_id = self.get_player_id(player_colour)
                if score[player_id] > vmax[player_id]:
                    vmax = score
                    best_a = move
            break
            
        
        print(str(player_colour) + " picked " + str(best_a) + " score was : " + str(vmax))
        # board_info.print_board(debug=True)
        
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
        elif player_colour == 'blue':
            return 'red'
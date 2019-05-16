from stickyFingers.utility_methods import *
import copy


class OpeningStrategy:

    def __init__(self, player, board_info):
        self.player = player
        self.board_info = board_info

    def move(self):

        moves_count = {}
        # for all our pieces
        for piece in self.player.pieces:
            # if it's in the starting zone
            if piece in self.board_info.player_starts(self.player.colour):
                # find this pieces moves
                possible_moves = find_moves(
                    piece, self.player.colour, self.board_info.board, self.board_info.pure_board)
                for move in possible_moves:
                    dest = move[1][1]
                    if dest not in self.board_info.player_starts(self.player.colour):
                        # if it's safe
                        if self.safe_move(move, self.player.colour, self.board_info):
                            # check how many collisions it has
                            moves_count[move] = self.closest_together(
                                move, self.player.colour, self.board_info)
        if len(moves_count) > 0:
            move_max_count = max(moves_count, key=moves_count.get)
            return move_max_count
        return None

    def closest_together(self, move, player_colour, board_info):

        count = 0
        piece = move[1][1]
        possible_radials = radial_moves(piece, 1)

        board_info_copy = copy.deepcopy(board_info)
        # get the next board state
        board_info_copy.update_board(player_colour, move)

        # for possible moves
        for radial_move in possible_radials:
            # if the move exists
            if radial_move in board_info.pure_board:
                # if there is a piece we are touching
                try:
                    collision_piece = board_info_copy.board[radial_move]
                    # if it is a piece we own, increase count
                    if collision_piece == player_colour:
                        count += 1
                except KeyError:
                    pass

        return count

    def safe_move(self, move, player_colour, board_info):

        if move[0] == 'EXIT':
            return True

        piece = move[1][1]
        possible_radials = radial_moves(piece, 1)

        board_info_copy = copy.deepcopy(board_info)
        # get the next board state
        board_info_copy.update_board(player_colour, move)

        # for possible moves
        for radial_move in possible_radials:
            # if the move exists
            if radial_move in board_info.pure_board:
                # if there is a piece we are touching
                try:
                    collision_piece = board_info_copy.board[radial_move]
                    # if it is not a piece we own, we can capture it
                    if collision_piece != player_colour:
                        # what if there is a person on the other side
                        # get jump moves for radial move and see if it can be captured

                        # print('{} at {} where {} would {}'.format(collision_piece, radial_move, player_colour, move))

                        # if the jump is occupied
                        jump_for_radials = jump_moves(
                            radial_move, board_info_copy.board, board_info.pure_board)
                        for jumps in jump_for_radials:
                            if jumped_coord(jumps) == piece:
                                # we cannot capture
                                return False

                except KeyError:
                    pass

        return True

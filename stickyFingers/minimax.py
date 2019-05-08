class MiniMax:
    def is_terminal_board(self, board):
        return True

    def heuristic(self, board):
        return 1

    def make_possible_board_states(self, board):
        return []

    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or self.is_terminal_board(board):

            return self.heuristic(board)

        possible_board_states = self.make_possible_board_states(board)

        if maximizing_player == 0:
            value = float("-inf")
            for board_state in possible_board_states:
                value = max(value, self.minimax(
                    board_state, depth - 1, maximizing_player + 1))
            return value
        else:
            value = float("inf")
            for board_state in possible_board_states:
                # take a third player into account
                if (maximizing_player + 1) > 2:
                    maximizing_player = 0
                value = min(value, self.minimax(
                    board_state, depth - 1, maximizing_player + 1))
            return value

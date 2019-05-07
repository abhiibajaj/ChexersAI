class Board:
    
    def __init__(self):
        self.pieceList = ['red', 'blue', 'green']
        self.board = self.create_pieces()
        print(self.board)
        
    
    def create_pieces(self):
        pieces = {}
        for piece in self.pieceList:
            start_coords = self.player_starts(piece)
            for coord in start_coords:
                pieces[coord] = piece
        return pieces
    
    def player_starts(self, colour):

        if colour == 'red':
            return ((-3,0), (-3,1), (-3,2), (-3,3))
        elif colour == 'blue':
            return ((0,3), (1,2), (2,1), (3, 0))
        elif colour == 'green':
            return ((0,-3), (1,-3), (2,-3), (3,-3))

    def update_board(self, colour, action):
        
        action_type = action[0]
        action_coords = action[1]

        if action_type == "PASS":
            pass
        
        elif action_type == "EXIT":
            del self.board[action_coords]

        else:
            src = action_coords[0]
            dest = action_coords[1]

            del self.board[src]
            self.board[dest] = colour

    def print_board(self, message="", debug=False, **kwargs):
        # Set up the board template:
        if not debug:
            # Use the normal board template (smaller, not showing coordinates)
            template = """# {0}
    #           .-'-._.-'-._.-'-._.-'-.
    #          |{16:}|{23:}|{29:}|{34:}| 
    #        .-'-._.-'-._.-'-._.-'-._.-'-.
    #       |{10:}|{17:}|{24:}|{30:}|{35:}| 
    #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    #    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
    #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
    # |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
    # '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
    #    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
    #       |{03:}|{08:}|{14:}|{21:}|{28:}| 
    #       '-._.-'-._.-'-._.-'-._.-'-._.-'
    #          |{04:}|{09:}|{15:}|{22:}|
    #          '-._.-'-._.-'-._.-'-._.-'"""
        else:
            # Use the debug board template (larger, showing coordinates)
            template = """# {0}
    #              ,-' `-._,-' `-._,-' `-._,-' `-.
    #             | {16:} | {23:} | {29:} | {34:} | 
    #             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
    #          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    #         | {10:} | {17:} | {24:} | {30:} | {35:} |
    #         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
    #      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
    #     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
    #     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
    #  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
    # | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
    # | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
    #  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
    #     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
    #     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
    #      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
    #         | {03:} | {08:} | {14:} | {21:} | {28:} |
    #         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
    #          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
    #             | {04:} | {09:} | {15:} | {22:} |   | input |
    #             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
    #              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

        # prepare the provided board contents as strings, formatted to size.
        ran = range(-3, +3+1)
        cells = []
        
        for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
            if qr in self.board:
                cell = str(self.board[qr]).center(5)
            else:
                cell = "     " # 5 spaces will fill a cell
            cells.append(cell)

        # fill in the template to create the board drawing, then print!
        board = template.format(message, *cells)
        print(board, **kwargs)
        
        
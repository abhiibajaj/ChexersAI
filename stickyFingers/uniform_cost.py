from stickyFingers.utility_methods import *
import heapq

class UniformCostSearch:

    def uniform_action(self, pieces, player_colour, board, pure_board):

        
        
        best_path = self.get_shortest_path(pieces, player_colour, board, pure_board)
        action = best_path[0]
        return action
    
    def get_shortest_path(self, pieces, player_colour, board, pure_board):
        all_paths = self.all_piece_paths(pieces, player_colour, board, 
                                         pure_board)
        
        best_path = self.shortest_path(all_paths)

        return best_path
    def shortest_path(self, paths):

        shortest_path = None
        shortest_len  = float("inf")

        for path in paths.values():
            path_len = len(path)
            if path_len < shortest_len:
                shortest_len = path_len
                shortest_path = path
        return shortest_path
            

    def all_piece_paths(self, pieces, player_colour, board, pure_board):
        """
        Helper function to apply uniform_cost_search to a list of pieces.
        """
        paths = {}
        # for each piece
        for piece in pieces:
            # make a path
            path = self.uniform_cost_search(piece, player_colour, board,
                                            pure_board)
            paths[piece] = path

        return paths
    

    def score_path(self, path):
        """
        Evaluates a given path with a heuristic that prefers jumps.

        Arguments:
        * `path` -- a list of a 3 tuple (piece_location, piece_destination, move_type)
        this path should contain the moves a piece should take to exit the board.
        """
        score = 0  
        if path == ("PASS", None):
            return float("-inf")

        # definitely exit if piece is in an exit
        if len(path) == 1:
            return float("inf")

        index = 0
        for move in path:
            try:
                action_type, _ = move
            except:
                print(path)
            # favour jumps in the near future
            if action_type == "JUMP":
                score += 1
                              
            index+=1

        return score

    def score_paths(self, paths):
        best_path = None
        best_score = float("inf")
        for path in paths.values():
            # skip empty paths
            if path == None:
                continue
            # score this path
            my_score = score_path(path)
            # keep the best
            if (best_path == None) or my_score < best_score:
                best_score = my_score
                best_path = path

        return best_path

    def uniform_cost_search(self, piece, player_colour, board, pure_board):
        """
        A uniform cost search algorithm for finding an exit for a given piece

        Arguments:
        * `piece` -- a 2 tuple of coordinates (x, y)
        * `board` -- a dictionary of { piece : player } representing the board state
        * `player` -- player is the String colour, ie. "red"
        """
        openSet = []
        heapq.heapify(openSet)

        closedSet = {}
        closedSet[piece] = None

        # push starting piece into open set
        # (heauristic + steps, steps, the piece)
        value = (0, 0, piece)
        heapq.heappush(openSet, value)

        while openSet:
            steps, _, the_piece = heapq.heappop(openSet)

            if is_exit(the_piece, player_colour):            
                # reconstruct the path that got us to the exit
                return self.reconstruct_path(the_piece, closedSet)

            # find the moves this piece can make
            
            my_moves = find_moves(the_piece, player_colour, board, 
                                    pure_board)
            
            # for each move
            for move in my_moves:
                steps_inc = steps + 1
                # _, dest, move_type = move
                (move_type, action_coords) = move
                if move_type == "EXIT":
                    dest = action_coords
                else:
                    dest = action_coords[1]
                distance_from_goal = steps_inc
                # see if it goes anywhere new
                if dest not in closedSet.keys():
                    # it does, add it to the heap
                    closedSet[dest] = (move_type, action_coords)
                    heapq.heappush(openSet, (steps_inc, distance_from_goal, dest))
        return ("PASS", None)


    def reconstruct_path(self, curr_coord, seen_moves):
        """
        Reconstruct a path from a uniform cost seach dictionary `seen_moves`
        """
        path = [("EXIT", curr_coord)]
        while seen_moves[curr_coord] != None:

            path.append(seen_moves[curr_coord])
            curr_coord = seen_moves[curr_coord][1][0]
        # reverse it, so it goes start to end
        return path[::-1]
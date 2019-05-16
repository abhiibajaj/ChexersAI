import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from chexersWrapper import chexersWrapper
from stickyFingers.utility_methods import *
from stickyFingers.board import *
from stickyFingers.uniform_cost import *


class stickyFingersKeras:
    def __init__(self):

        self.pure_board = Board().get_pure_board()
        self.ucs = UniformCostSearch()
        self.game = chexersWrapper()

        self.goal_steps = 500
        self.score_requirement = 60
        self.intial_games = 1000
        self.colour = 'blue'
        self.gamewon = False

    def reset(self):
        self.gamewon = False

    def handle_gameerror(self):
        self.gamewon = False
        print("Game ended without winner")

    def handle_gameover(self, player):
        if self.colour == player:
            self.gamewon = True
        print("Game winner", player)

    def handle_turn(self, player, state):
        #print("State: ", state)

        my_pieces = set()
        for piece, colour in state.items():
            if colour == player:
                my_pieces.add(piece)

        """
        # uniform cost search
        action_to_take = self.ucs.uniform_action(
            my_pieces, player, state,
            self.pure_board
        )
                
        return action_to_take
        """

        # make random moves
        if len(my_pieces) > 0:
            moves = []
            for piece in my_pieces:
                my_moves = find_moves(
                    piece, player, state, self.pure_board)
                moves += my_moves

            if len(moves) > 0:
                random_move = random.choice(moves)
                return random_move
            else:
                return ('PASS', None)
        else:
            return ('PASS', None)

    def model_data_preparation(self):
        training_data = []
        game_memory = []
        # play initial_games amount of games
        for game_index in range(self.intial_games):
            score = 0
            game_memory = self.game.run(self.handle_gameover,
                                        self.handle_turn,
                                        self.handle_gameerror)
            # get games that lead to a win
            if self.gamewon:
                training_data += game_memory

            self.reset()

        return training_data

    def main(self):
        training_data = self.model_data_preparation()
        print(training_data)


stickyFingersKeras().main()

from stickyFingersJump0.heuristic_jump import *
from stickyFingersJump0.heuristic_jump_v0 import *


class Heurisitic:

    def __new__(self, strategy):
        if strategy == "Jumpv0":
            return HeuristicJump0()
        elif strategy == "Jump":
            return HeuristicJump()

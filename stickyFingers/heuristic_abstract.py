from stickyFingers.heuristic_jump import *
from stickyFingers.heuristic_jump_v0 import *


class Heurisitic:

    def __new__(self, strategy):
        if strategy == "Jumpv0":
            return HeurisiticJump0()
        elif strategy == "Jump":
            return HeuristicJump()


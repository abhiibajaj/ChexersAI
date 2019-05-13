from stickyFingers.heuristic_manhattan import *
from stickyFingers.heuristic_jump import *

class Heurisitic:

    def __new__(self, strategy):
        if strategy == "Manhattan":
            return HeurisiticManhattan()
        elif strategy == "Jump":
            return HeuristicJump()

a = Heurisitic("Manhattan")
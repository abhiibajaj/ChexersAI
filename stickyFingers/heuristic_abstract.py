from stickyFingers.heuristic_manhattan import *
class Heurisitic:

    def __new__(self, type):
        if type == "Manhattan":
            return HeurisiticManhattan()

a = Heurisitic("Manhattan")
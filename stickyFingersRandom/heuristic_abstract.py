from stickyFingersRandom.heuristic_jump import HeuristicJump
from stickyFingersRandom.heuristic_jump_v0 import HeuristicJump0


class Heurisitic:
    """
    Heuristic Factory
    """

    def __new__(self, strategy):
        return HeuristicJump()

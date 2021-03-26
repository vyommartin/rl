import random


class Player(object):
    """docstring for Player
    AI chooses which piece to play here
    Available data:
      piecces: the set of movable pieces for AI player
      self.board: Game board with complete state"""

    def __init__(self):
        super(Player, self).__init__()

    def choose(self, pieces, step, board):
        return random.choice(pieces)

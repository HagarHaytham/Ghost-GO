import enum
from collections import namedtuple

__all__ = [
    'Player',
    'Point',
]

class Player(enum.Enum):
    black = 1
    white = 2
    
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

class Point(namedtuple('Point', 'row col')): # namedtuple to you access the coordinates as point.row and point.col

    # Return the neighbours of a point
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1), 
            Point(self.row, self.col + 1),
        ]

    def __deepcopy__(self, memodict={}):
        # These are very immutable.
        return self
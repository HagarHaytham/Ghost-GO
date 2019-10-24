import numpy as np
from collections import namedtuple


# should be imported from game rules ????
class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

class OnePlaneEncoder():
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1
       
    def encode(self, game_state): 
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                   continue
                if go_string.color == next_player:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = 1
        return board_matrix

    def encode_point(self, point): 
        return self.board_width * (point.row -1)+ (point.col -1)
    def decode_point_index(self, index): 
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)
    def num_points(self):
        return self.board_width * self.board_height
    def shape(self):
        return self.num_planes, self.board_height, self.board_width
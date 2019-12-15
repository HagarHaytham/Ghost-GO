
import numpy as np

from .gostuff.goboard_fast import Move, Point


class SevenPlaneEncoder():
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 7

    def encode(self, game_state):
        board_tensor = np.zeros(self.shape())
        base_plane = {game_state.next_player: 0, # what ??
                      game_state.next_player.other: 3}
        for row in range(self.board_height):
            for col in range(self.board_width):
                p = Point(row=row + 1, col=col + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    if game_state.does_move_violate_ko(game_state.next_player,
                                                       Move.play(p)):
                        board_tensor[6][row][col] = 1  # 7th plane is invalid moves (KO RULE)
                else:
                    liberty_plane = min(3, go_string.num_liberties) - 1  # 1st plane (1 liberty) and so on
                    liberty_plane += base_plane[go_string.color]
                    board_tensor[liberty_plane][row][col] = 1  
        return board_tensor

    def encode_point(self, point):
        return self.board_width * (point.row - 1) + (point.col - 1)

    def decode_point_index(self, index):
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width

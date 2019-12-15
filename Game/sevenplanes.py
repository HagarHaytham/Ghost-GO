
import numpy as np

#from .gostuff.goboard_fast import Move, Point
from dlgo.goboard_slow import Move ,Point
import time 

TotalCount = 0
TotalTime = 0
GoStringTime = 0
ZerosTime = 0
ViolateTime = 0
DeepTime = {'time': 0}
    
class SevenPlaneEncoder():
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 7

    def encode(self, game_state):
        global ZerosTime,TotalCount, TotalTime, GoStringTime, ViolateTime,DeepTime
        StartTime = time.time()
        board_tensor = np.zeros(self.shape())
        ZerosTime += time.time() - StartTime
        base_plane = {game_state.next_player: 0, # what ??
                      game_state.next_player.other: 3}
        for row in range(self.board_height):
            for col in range(self.board_width):
                p = Point(row=row + 1, col=col + 1)
                GoStringStartTime = time.time()
                go_string = game_state.board.get_go_string(p)
                GoStringTime += time.time() - GoStringStartTime
                if go_string is None:
                    ViolateStartTime = time.time()
                    if game_state.does_move_violate_ko(game_state.next_player,
                                                       Move.play(p),DeepTime):
                        board_tensor[6][row][col] = 1  # 7th plane is invalid moves (KO RULE)
                    ViolateTime += time.time() - ViolateStartTime
                else:
                    liberty_plane = min(3, go_string.num_liberties) - 1  # 1st plane (1 liberty) and so on
                    liberty_plane += base_plane[go_string.color]
                    board_tensor[liberty_plane][row][col] = 1
        TotalTime += time.time() - StartTime
        TotalCount += 1
        
        if TotalCount == 100:
            # print('encode', TotalTime)
            # print('zeros', ZerosTime)
            # print('GoString', GoStringTime)
            # print('violate', ViolateTime)
            # print('DeepTime', DeepTime['time'])
            # print()
            TotalCount = 0
            TotalTime = 0
            GoStringTime = 0
            ZerosTime = 0
            ViolateTime = 0
            DeepTime = {'time': 0}
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

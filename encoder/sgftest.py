from sgf.sgf import Sgf_game 
# should be imported from gamerules part
from gostuff.goboard_fast import GameState, Move
# from dlgo.goboard_fast import GameState, Move
from gostuff.gotypes import Point
from gostuff.utils import print_board
sgf_content = "(;GM[1]FF[4]SZ[9];B[ee];W[ef];B[ff]" +";W[df];B[fe];W[fc];B[ec];W[gd];B[fb])"
with open ("2002-01-01-1.sgf", "r") as myfile:
    sgf_content2=myfile.read() 
sgf_game = Sgf_game.from_string(sgf_content2) 
game_state = GameState.new_game(19)
for item in sgf_game.main_sequence_iter(): 
    color, move_tuple = item.get_move() 
if color is not None and move_tuple is not None:
    row, col = move_tuple
    point = Point(row + 1, col + 1)
    move = Move.play(point)
    game_state = game_state.apply_move(move)
    print_board(game_state.board)
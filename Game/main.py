from dlgo.agent import naive
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import interface
from enum import Enum
from  MCTS import monte_carlo_tree_search
from dlgo.scoring import compute_game_result
import time
import numpy as np 
board_size = 19
num_rounds = 10
game_mode = 0
depth = 10
consequitive_passes = 0
opponont_resigns = False
rows = [19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
cols = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
class modes(Enum):
   AIvsAI=0
   AIvsHuman=1
   AIvsAI_test=2

def get_game_mode_from_gui():
    global game_mode
    game_mode = interface.get_game_mode()
    game = goboard.GameState.new_game(board_size) 
    player = gotypes.Player.black
    opponent = gotypes.Player.white
    captures = {
        gotypes.Player.black: 0,
        gotypes.Player.white: 0,
    } 

    if(game_mode == modes.AIvsAI ):  # PC mode  
        #get player color from server
        pass
    elif( game_mode == modes.AIvsHuman ):
        player , opponent = get_game_mode_from_gui()
    elif (game_mode == modes.AIvsAI_test): # trainer test mode start from a certain state
        # game_board = np.zeros((board_size,board_size))
        # fill matrix somehow
        # send_state(game_board)
        # get player color from server
        pass        
    return game , captures , player , opponent

def get_player_color_from_gui():
    player = gotypes.Player.black
    opponent = gotypes.Player.white
    opponent_color = interface.get_opponent_color()
    if(opponent_color == 0):
        opponent = gotypes.Player.black
        player = gotypes.Player.white
    return player ,opponent

def get_opponent_game_from_gui(current_state,captures,opponent):
    global consequitive_passes
    global opponont_resigns
    global rows
    global cols
    new_game_state =0 
    point = 0
    decision =interface.get_opponent_move()
    if decision[0] == 0 : # play  
        consequitive_passes = 0
        x = cols.index(decision[2])+1
        y = rows.index(decision[4])+1
        point =  gotypes.Point(x,y)
        move = goboard.Move(point)
        new_game_state , prisoners  = current_state.apply_move(move)
        capture = 0
        if len(prisoners) > 0:
            capture = prisoners[0]
        captures[opponent]+=capture
    elif decision[1] == 1 :  # opponont_opponont_resignss
        opponont_resigns = True
    elif decision[2] == 2 : # pass
        consequitive_passes+=1
    return new_game_state , captures , point

def send_move_to_gui(decision,point):
    global consequitive_passes
    if(decision == 0): # play
        consequitive_passes = 0 
        col = cols[point.X-1]
        row = rows[point.Y-1]
        move = '0'+'#'+str(row)+'-'+str(col)
    elif decision == 1: # player_resigns 
        move = '1'
    elif decision == 2: # pass
        consequitive_passes+=1
        move = '2'
    interface.send_ghost_move(move)
    return  
    
def send_valid_moves_to_gui(game_state):
    legal_moves = game_state.legal_moves()
    moves=np.array(len(legal_moves)-2,2)
    for k in range(len(moves)) : 
        move = legal_moves[k]
        moves[k][0]= move.point.X
        moves[k][1]= move.point.Y
    interface.send_valid_moves(moves)
    return

def send_score_to_gui(game_result,winner,player,reason):
    black_score = game_result[0]
    white_score = game_result[1]
    w=1
    O_score = black_score
    G_Score = white_score
    if( winner == gotypes.Player.black):
        w=0
    if( player == gotypes.Player.black):
        O_score = white_score
        G_Score = black_score
    interface.send_score(str(w),O_score,G_Score,reason)
    return
def send_captures_to_gui(captures):
    b = captures[gotypes.Player.black]
    w = captures[gotypes.Player.black]
    # send to gui , i still can't know the position of captures
def main():
    global consequitive_passes
    global opponont_resigns
    game , captures ,player ,opponent = get_game_mode_from_gui()
    first_game = False
    if( opponent == gotypes.Player.white):
        first_game = True
    if(game_mode == modes.AIvsHuman):
        while ( not game.is_over()):
            print_board(game.board)
            start = time.time()
            point = -1
            if(not first_game):
                game , captures , point  =  get_opponent_game_from_gui(game,captures,opponent)
                send_captures_to_gui(captures)
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            game , captures , play_coords= monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            send_captures_to_gui(captures)
            decision = 0
            point = gotypes.Point(play_coords.X,play_coords.Y)
            send_move_to_gui(decision , point)
            if(consequitive_passes == 2):
                break
            end = time.time()
            print(end - start)
    else:  # AI vs AI
        while ( not game.is_over()):
            print_board(game.board)
            start = time.time()
            point = -1
            if(not first_game):
                # TODO get opponent game from server
                send_captures_to_gui(captures)
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            game , captures , play_coords = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            send_captures_to_gui(captures)
            decision = 0
            point = gotypes.Point(play_coords.X,play_coords.Y)
            send_move_to_gui(decision , point)
            # TODO send move to server , note  point.x = 1 to 19 , point.y = 1 to 19
            if(consequitive_passes == 2):
                break
            end = time.time()
            print(end - start)

    game_result,winner,score = game.winner(captures)
    reason = 'IDK !'
    send_score_to_gui(game_result,winner,score,reason)
    if winner == gotypes.Player.black:
        print("Black is the WINNER!!!!")
    else:
        print("White is the WINNER!!!!")

    print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])

if __name__ == '__main__':
    main()
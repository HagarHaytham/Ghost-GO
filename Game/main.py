from dlgo.agent import naive
from dlgo import goboard_slow as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import interface
from  MCTS import monte_carlo_tree_search
import time
import numpy as np 
board_size = 19
num_rounds = 10
depth = 10
opponent_consequitive_passes = 0
player_consequitive_passes = 0
opponont_resigns = False

def game_mode():
    game_mode = 0  
    game_mode = interface.get_game_mode()
    game = 0
    captures =0
    if(game_mode == 0 or game_mode == 1):  # PC mode  
        game = goboard.GameState.new_game(board_size) 
        captures = {
            gotypes.Player.black: 0,
            gotypes.Player.white: 0,
        } 
    
    elif (game_mode == 1):  # trainer mode  AI VS human
        pass
    elif (game_mode == 2): # trainer test mode start from a certain state
        game_board = np.zeros((board_size,board_size))
        
        # fill matrix somehow
        # send_state(game_board)
        pass        
    return game , captures

def get_player_color():
    opponent  =interface.get_opponent_color()
    opponent = 0
    if(opponent == 0):
        return gotypes.Player.white , gotypes.Player.black
    return gotypes.Player.black , gotypes.Player.white

def get_next_state(current_state,captures,opponent):
    global consequitive_passes
    global opponont_opponont_resignss
    decision=[0,'#',1,'-',4]
    new_game_state =0 
    point =0
    decision =interface.get_opponent_move()
    if decision[0] == 0 : # play  
        consequitive_passes = 0
        point =  gotypes.Point(decision[2],decision[4])
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

def send_move(decision,point):
    global player_consequitive_passes
    if(decision == 0): # play
        player_consequitive_passes = 0 
        move = '0'+'#'+str(point.X)+'-'+str(point.Y)
    elif decision == 1: # player_resigns 
        move = '1'
    elif decision == 2: # pass
        move = '2'
    iterface.send_ghost_move(move)
    return  
    
def send_valid_moves_to_gui(game_state):
    legal_moves = game_state.legal_moves()
    moves=np.array(len(legal_moves)-2,2)
    for k in range(len(moves)) : 
        move = legal_moves[k]
        moves[k][0]= move.point.X
        moves[k][1]= move.point.Y
    iterface.send_valid_moves(moves)
    return

def send_score_to_gui(score):
    iterface.send_score(score)
    return

def main():
    global opponent_consequitive_passes
    global player_consequitive_passes
    global opponont_resigns
    game , captures = game_mode()
    player , opponent = get_player_color() 
    old_game_score = 0
    
    while ( not game.is_over()):

        print_board(game.board)

        start = time.time()
        game , captures , point  =  get_next_state(game,captures,opponent)
        if(opponent_consequitive_passes == 2 or opponont_resigns == True ):
            break
        game , captures , play_coords= monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
        _winner ,this_game_score = game.winner(captures)
        decision = 0
        point =Point(play_coords.X,play_coords.Y)
        if(old_game_score >= this_game_score ):  #pass game
            decision = 2
            point = -1
            player_consequitive_passes+=1
        send_move(decision , point)
        if(player_consequitive_passes == 2):
            break
        end = time.time()
        print(end - start)

    winner,score = game.winner(captures)
    
    if winner == gotypes.Player.black:
        print("Black is the WINNER!!!!")
    else:
        print("White is the WINNER!!!!")

    print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])

if __name__ == '__main__':
    main()
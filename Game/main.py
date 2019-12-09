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
class modes(Enum):
   AIvsAI=0
   AIvsHuman=1
def get_game_mode_from_gui():
    global game_mode
    game_mode = interface.get_game_mode()
    game = goboard.GameState.new_game(board_size) 
    player = '0'
    opponent = '1'
    captures = {
        '0': 0,
        '1': 0,
    } 
    if(game_mode == modes.AIvsAI ):  # PC mode  
        #get player color from server
        pass
    elif( game_mode == modes.AIvsHuman ):
        player , opponent = get_player_color_from_gui()
    # elif (game_mode == modes.AIvsAI_test): # trainer test mode start from a certain state
    #     # game_board = np.zeros((board_size,board_size))
    #     # fill matrix somehow
    #     # send_state(game_board)
    #     # get player color from server
    #     pass        
    return game , captures , player , opponent

def get_player_color_from_gui():
    player = '0'
    opponent = '1'
    opponent_color = interface.get_opponent_color()
    if(opponent_color == '0'):
        player = '1'
    return player ,opponent

def get_opponent_game_from_gui(current_state,captures,opponent):
    global consequitive_passes
    global opponont_resigns
    new_game_state =0 
    point = 0
    decision =interface.get_opponent_move()
    if decision[0] == '0' : # play  
        consequitive_passes = 0
        point =  gotypes.Point(int(decision[2]),int(decision[4]))
        move = goboard.Move(point)
        new_game_state , prisoners  = current_state.apply_move(move)
        capture = 0
        if len(prisoners) > 0:
            capture = prisoners[0]
        captures[opponent]+=capture
    elif decision[1] == '1' :  # opponont_opponont_resignss
        opponont_resigns = True
    elif decision[2] == '2' : # pass
        consequitive_passes+=1
    return decision[0] , new_game_state , captures , point

def send_move_to_gui(decision,point,b_time,w_time,color):
    global consequitive_passes
    if(decision == 0): # play
        consequitive_passes = 0 
        move = '0'+'#'+str(point.X)+'-'+str(point.Y)
    elif decision == 1: # player_resigns 
        move = '1'
    elif decision == 2: # pass
        consequitive_passes+=1
        move = '2'
    interface.send_move(move,color,b_time,w_time)
    return  
def send_board_to_gui(decision,board):    
    stone_list=[]
    if decision == '0':
        for i in range(19):
            for j in range(19):
                stone = gotypes.Point(i,j)
                color = board.get(stone)
                if( color != None):
                    stone_list.append([i,j,color])
    interface.update_board(stone_list)
    pass
# def update_board():
#     pass
def send_valid_moves_to_gui(game_state):
    legal_moves = game_state.legal_moves()
    moves=np.array(len(legal_moves)-2,2)
    for k in range(len(moves)) : 
        move = legal_moves[k]
        moves[k][0]= str(move.point.X)
        moves[k][1]= str(move.point.Y)
    interface.send_valid_moves(moves)
    return

def send_score_to_gui(game_result,player,reason):
    black_score = str(game_result[0])
    white_score = str(game_result[1])
    O_score = black_score
    G_Score = white_score
    if( player == '0'):
        O_score = white_score
        G_Score = black_score
    interface.send_score(O_score,G_Score,reason)
    return
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
                decision , game , captures , point  =  get_opponent_game_from_gui(game,captures,opponent)
                b_time = 0
                w_time = 0
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            game , captures , play_coords= monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            decision = 0
            point = gotypes.Point(play_coords.X,play_coords.Y)
            b_time = 0
            w_time = 0
            send_move_to_gui(decision,point,b_time,w_time,player)  
            send_board_to_gui(decision,game.board)
          
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
                # TODO get opponent game from server  , and remaining time for black b_time and white w_time
                b_time = 0
                w_time = 0
                send_move_to_gui(decision,point,b_time,w_time,opponent)            
                send_board_to_gui(decision,game.board)
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            game , captures , play_coords = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            decision = 0
            point = gotypes.Point(play_coords.X,play_coords.Y)
            b_time = 0
            w_time = 0
            # TODO send move to server , note  point.x = 1 to 19 , point.y = 1 to 19

            send_move_to_gui(decision,point,b_time,w_time,player)         
            send_board_to_gui(decision,game.board)   
            if(consequitive_passes == 2):
                break
            end = time.time()
            print(end - start)
    game_captures ={
        gotypes.Player.black : captures[0],
        gotypes.Player.white : captures[1]
    }
    game_result,winner,score = game.winner(game_captures)
    reason = 'IDK !'
    send_score_to_gui(game_result,score,reason)
    if winner == '0':
        print("Black is the WINNER!!!!")
    else:
        print("White is the WINNER!!!!")

    print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])

if __name__ == '__main__':
    main()
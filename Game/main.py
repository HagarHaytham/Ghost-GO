from dlgo.agent import naive
from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move , coords_from_point2
import interface
import copy 
from enum import Enum
from  MCTS import monte_carlo_tree_search
from dlgo.scoring import compute_game_result
import time
import numpy as np
import elevenplanes
import predict
#intializations
board_size = 19
num_rounds = 10
game_mode = 0
depth = 10
consequitive_passes = 0
opponont_resigns = False

class modes(Enum): #check ENUM
   AIvsAI=0
   AIvsHuman=1
   
def get_game_mode_from_gui():
    global game_mode
    game_mode = int(interface.get_game_mode())
    # print("game mode received --> ", game_mode)
    game = goboard.GameState.new_game(board_size) 
    player = '0'
    opponent = '1'
    captures = {
        '0': 0,
        '1': 0,
    } 
    if(game_mode == 1 ):  # PC mode  
        #get player color from server
        # print('ai vs ai')
        pass
    elif( game_mode == 0 ):
        # print('ai vs human')
        player , opponent = get_player_color_from_gui()
    # elif (game_mode == modes.AIvsAI_test): # trainer test mode start from a certain state
    #     # game_board = np.zeros((board_size,board_size))
    #     # fill matrix somehow
    #     # send_state(game_board)
    #     # get player color from server
    #     pass        
    return game , captures , player , opponent

def get_player_color_from_gui():
    # print("get_player_color_from_gui")
    player = '0'
    opponent = '1'
    opponent_color = interface.get_opponent_color()
    if(opponent_color == '0'):
        player = '1'
    return player ,opponent

def get_opponent_game_from_gui(current_state,captures,opponent):
    # print("get_opponent_game_from_gui")
    global consequitive_passes
    global opponont_resigns
    new_game_state= current_state
    point = 0
    decision = interface.get_opponent_move().split('#')
    if decision[0] == '0' : # play  
        consequitive_passes = 0
        print(decision)
        pos = decision[1].split('-')
        point =  gotypes.Point(int(pos[0]),int(pos[1]))
        move = goboard.Move(point)
        # print(">>>> move", move.point)
        new_game_state , prisoners  = current_state.apply_move(move)
        captures[opponent]+=prisoners
    elif decision[0] == '1' :  # opponont_opponont_resignss
        opponont_resigns = True
    elif decision[0] == '2' : # pass
        consequitive_passes+=1
    return decision[0] , new_game_state , captures , point

def send_move_to_gui(decision,point,b_time,w_time,color):
    # print("send_move_to_gui")
    global consequitive_passes
    if(decision == 0): # play
        consequitive_passes = 0 
        move = '0'+'#'+str(point.col)+'-'+str(point.row)
        print('sent point ' ,point)
    elif decision == 1: # player_resigns 
        move = '1'
    elif decision == 2: # pass
        consequitive_passes+=1
        move = '2'
    interface.send_move(move,color,str(b_time),str(w_time))
    return  
def send_board_to_gui(decision,board): 
    print("send_board_to_gui")   
    stone_list = []
    if decision == '0':
        for i in range(19):
            for j in range(19):
                stone = gotypes.Point(i,j)
                color = board.get(stone)
                if( color != None):
                    c='0'
                    if color == gotypes.Player.white :
                        c ='1'
                    stone_list.append([i,j,c])
    interface.update_board(stone_list)
    pass
# def update_board():
#     pass
def send_valid_moves_to_gui(game_state):
    print("send_valid_moves_to_gui")
    legal_moves = game_state.legal_moves()
    moves=legal_moves[0:len(legal_moves)-2]
    list = []
    for k in range(len(moves)) : 
        move = legal_moves[k]
        col = str(move.point.col)
        row = str(move.point.row)
        list.append([col,row])
    interface.send_valid_moves(list)
    return

def send_score_to_gui(game_result,player,reason):
    print("send_score_to_gui|")
    #print(game_result[0])
    print(type(game_result))
    black_score = str(game_result[0])
    white_score = str(game_result[1])
    O_score = black_score
    G_Score = white_score
    if( player == '0'):
        O_score = white_score
        G_Score = black_score
    print('scores ',O_score,G_Score)
    interface.send_score(O_score,G_Score,reason)
    return
def recommend_move(game_state):
    state = elevenplanes.ElevenPlaneEncoder((19,19))
    state = state.encode(game_state)
    state = np.expand_dims(state,axis=0)
    probability_matrix=predict.model.predict(state)[0]
    probability_matrix = np.reshape(probability_matrix, (-1, 19))
    new_point = -1
    while True:
        max = probability_matrix.max()
        coordinates = np.where(probability_matrix == max)
        row = coordinates[0][0]
        col = coordinates[1][0]
        probability_matrix[row][col]= 0
        new_point = gotypes.Point( row=row+1,col=col+1)
        move = goboard.Move(new_point)
        if game_state.is_valid_move(move):
            break
    new_game_state , prisoners  = game_state.apply_move(move)
    # print('in main',type(new_game_state))
    return new_game_state , new_point
def compare_state(state1,state2,captures,player):
    c ={ 
        gotypes.Player.black : captures['0'],
        gotypes.Player.white : captures['1']
    }
    game_result1 = compute_game_result(state1,c)
    game_result2 = compute_game_result(state2,c)
    black_score1 = str(game_result1[0])
    white_score1 = str(game_result1[1])
    O_score1 = black_score1
    black_score2 = str(game_result2[0])
    white_score2 = str(game_result2[1])
    O_score2 = black_score2
    if( player == '0'):
        O_score1 = white_score1
        O_score2 = white_score2
    if(O_score1 > O_score2 ):
        return True
    return False
def send_congrats():
    congrats_msg ='Nice Move !!'
    interface.send_congrate(congrats_msg)
def send_recommended_move(decision,point):
    msg = str(decision)
    if(decision ==0):
        msg = msg+'#'+str(point.col)+'-'+str(point.row)
    else:
        msg = msg+'#0'
    interface.send_recommended_move(msg)
def main():
    global consequitive_passes
    global opponont_resigns
    game , captures ,player ,opponent = get_game_mode_from_gui()
    first_game = False
    if( opponent == gotypes.Player.white):
        first_game = True
    if(game_mode == 0 ):
        while ( not game.is_over()):
            # print_board(game.board)
            start = time.time()
            point = -1
            if(not first_game):
                send_valid_moves_to_gui(game)
                old_game = copy.deepcopy(game)
                recommended , recommended_move = recommend_move(old_game)
                old_captures = copy.copy(captures[opponent])
                decision , game , captures , point  =  get_opponent_game_from_gui(game,captures,opponent)
                result = compare_state(recommended,game,captures,player)
                if(result == True):
                    send_recommended_move(decision,point)
                    pass
                else:
                    send_congrats()
                    pass
                if( captures[opponent] > old_captures):
                    send_board_to_gui(decision,game.board)      
                b_time = 0
                w_time = 0
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            old_captures = copy.copy(captures[player])
            game , captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            # print('after monto carlo')
            decision = 0
            b_time = 0
            w_time = 0
            send_move_to_gui(decision,play_point,b_time,w_time,player)  
            if(captures[player] > old_captures):
                send_board_to_gui(decision,game.board)
            if(consequitive_passes == 2):
                break
            end = time.time()
            # print(end - start)
    elif(game_mode == 1 ):  # AI vs AI
        while ( not game.is_over()):
            # print_board(game.board)
            start = time.time()
            point = -1
            if(not first_game):
                old_captures = copy.copy(captures[opponent])

                # TODO get opponent game from server  , and remaining time for black b_time and white w_time
                b_time = 0
                w_time = 0
                send_move_to_gui(decision,point,b_time,w_time,opponent)
                if(captures[opponent] > old_captures):            
                    send_board_to_gui(decision,game.board)  
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            old_captures = copy.copy(captures[player])
            game , captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            decision = 0
            b_time = 0
            w_time = 0
            # TODO send move to server 
            send_move_to_gui(decision,play_point,b_time,w_time,player)         
            if(captures[player] > old_captures):
                send_board_to_gui(decision,game.board)   
            if(consequitive_passes == 2):
                break
            end = time.time()
            # print(end - start)
    game_captures ={
        gotypes.Player.black : captures['0'],
        gotypes.Player.white : captures['1']
    }
    if(game_mode == 0):
        #game_result,winner,score = game.winner(game_captures)
        game_result,score = game.winner(game_captures)
        reason = 'IDK !'
    else:
        # get score from server
        print("///////////////")
        pass
    send_score_to_gui(game_result,player,reason)
    # if winner == '0':
    #     print("Black is the WINNER!!!!")
    # else:
    #     print("White is the WINNER!!!!")

    # print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])

if __name__ == '__main__':
    main()
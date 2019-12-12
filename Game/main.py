from Game.dlgo.agent import naive
from Game.dlgo import goboard_fast as goboard
from Game.dlgo import gotypes
from Game.dlgo.utils import print_board, print_move , coords_from_point2
import Game.interface
from enum import Enum
from  Game.MCTS import monte_carlo_tree_search
from Game.dlgo.scoring import compute_game_result
import Game.client_game as client_game
import Game.client as client
import time
import numpy as np

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
    game_mode = int(Game.interface.get_game_mode())
    print("game mode received --> ", game_mode)
    game = goboard.GameState.new_game(board_size) 
    player = '0'
    opponent = '1'
    captures = {
        '0': 0,
        '1': 0,
    } 
    if(game_mode == 1 ):  # PC mode  
        #get player color from server
        print('ai vs ai')
        pass
    elif( game_mode == 0 ):
        print('ai vs human')
        player , opponent = get_player_color_from_gui()
    # elif (game_mode == modes.AIvsAI_test): # trainer test mode start from a certain state
    #     # game_board = np.zeros((board_size,board_size))
    #     # fill matrix somehow
    #     # send_state(game_board)
    #     # get player color from server
    #     pass        
    return game , captures , player , opponent

def get_player_color_from_gui():
    print("get_player_color_from_gui")
    player = '0'
    opponent = '1'
    opponent_color = Game.interface.get_opponent_color()
    if(opponent_color == '0'):
        player = '1'
    return player ,opponent

def get_opponent_game_from_gui(current_state,captures,opponent):
    print("get_opponent_game_from_gui")
    global consequitive_passes
    global opponont_resigns
    point = 0
    decision = Game.interface.get_opponent_move().split('#')
    if decision[0] == '0' : # play  
        consequitive_passes = 0
        print(decision)
        pos = decision[1].split('-')
        point =  gotypes.Point(int(pos[0]),int(pos[1]))
        move = goboard.Move(point)
        print(">>>> move", move.point)
        new_game_state , prisoners  = current_state.apply_move(move)
        capture = 0
        if len(prisoners) > 0:
            capture = prisoners[0]
        captures[opponent]+=capture
    elif decision[0] == '1' :  # opponont_opponont_resignss
        opponont_resigns = True
    elif decision[0] == '2' : # pass
        consequitive_passes+=1
    return decision[0] , new_game_state , captures , point

def send_move_to_gui(decision,point,b_time,w_time,color):
    print("send_move_to_gui")
    global consequitive_passes
    if(decision == 0): # play
        consequitive_passes = 0 
        move = '0'+'#'+str(point.col)+'-'+str(point.row)
    elif decision == 1: # player_resigns 
        move = '1'
    elif decision == 2: # pass
        consequitive_passes+=1
        move = '2'
    Game.interface.send_move(move,color,str(b_time),str(w_time))
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
    Game.interface.update_board(stone_list)
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
    Game.interface.send_valid_moves(list)
    return

def send_score_to_gui(game_result,player,reason):
    print("send_score_to_gui|")
    black_score = str(game_result[0])
    white_score = str(game_result[1])
    O_score = black_score
    G_Score = white_score
    if( player == '0'):
        O_score = white_score
        G_Score = black_score
    Game.interface.send_score(O_score,G_Score,reason)
    return

def READY_configuration(game):
    # Game Configuration
    parameters = client.handle_ready()
    ''' 
        Start Game configuration
    '''
    # Initial State
    for y,row in enumerate(parameters['initailState']['board']):
        for x,color in enumerate(row):
            if color == '.':
                continue
            game.next_player = gotypes.Player.black if color == 'B' else gotypes.Player.white
            move = goboard.Move(gotypes.Point((y+1,x+1)))
            game,_ = game.apply_move(move)
    
    captures = {
        gotypes.Player.black : parameters['initialState']['players']['B']['prisoners'],
        gotypes.Player.white : parameters['initialState']['players']['W']['prisoners'],
    }
    
    remainingTime = {
        gotypes.Player.black : parameters['initialState']['players']['B']['remainingTime'],
        gotypes.Player.white : parameters['initialState']['players']['W']['remainingTime'],
    }

    game.next_player = gotypes.Player.black if parameters['initailState']['turn'] == 'B' else gotypes.Player.white
    # fill the board with move logs
    for logEntry in parameters['moveLog']:
        move = logEntry["move"]
        deltaTime = move['deltaTime']
        if move['type'] == 'pass':
            move = goboard.Move(is_pass=True)
        elif move['type'] == 'resign':
            move = goboard.Move(is_resign=True)
        else:
            col = move['point']['column']
            row = move['point']['row']
            move = goboard.Move(gotypes.Point((row,col)))

        remainingTime[game.next_player] -= deltaTime
        game,numberOfCaptures = game.apply_move(move)
        if len(numberOfCaptures) > 0:
            if game.next_player == gotypes.Player.white:
                captures[gotypes.Player.black] += numberOfCaptures[0]
            else:
                captures[gotypes.Player.white] += numberOfCaptures[0]

    ourColor = gotypes.Player.black if parameters['ourColor'] == 'B' else gotypes.Player.white
    ''' 
        End Game configuration
    '''

    return game, captures, remainingTime, ourColor

def THINKING(game):
    print_board(game.board)
    start = time.time()
    point = -1
    player = game.next_player
    game , captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
    decision = 0
    b_time = 0
    w_time = 0
    
    play_move = goboard.Move(play_point)
    client.handle_thinking()
    client_game.get_move_from_game(play_move)
    client_game.get_parameters_from_client_game()
    # TODO send move to server 
    send_move_to_gui(decision,play_point,b_time,w_time,player)         
    send_board_to_gui(decision,game.board)   
    if(consequitive_passes == 2):
        break
    end = time.time()
    print(end - start)
    return game

def AI_vs_AI(game):
    response = client.handle_init()
    if client.current_state == client.states['END']:
        # handle results
        return

    game, captures, remainingTime, ourColor = READY_configuration(game)
    if client.current_state == client.states['END']:
        # handle results
        return

    while not game.is_over():
        if game.next_player == ourColor:
            THINKING()
        else:
            IDLE()
    

def main():
    global consequitive_passes
    global opponont_resigns
    game, captures, player, opponent = get_game_mode_from_gui()
    first_game = False

    if( opponent == gotypes.Player.white):
        first_game = True
    if(game_mode == 0 ):
        while ( not game.is_over()):
            print_board(game.board)
            start = time.time()
            point = -1
            if(not first_game):
                send_valid_moves_to_gui(game)
                decision , game , captures , point  =  get_opponent_game_from_gui(game,captures,opponent)
                send_board_to_gui(decision,game.board)
                b_time = 0
                w_time = 0
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            else:
                first_game = False
            game , captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            print('after monto carlo')
            decision = 0
            b_time = 0
            w_time = 0
            send_move_to_gui(decision,play_point,b_time,w_time,player)  
            send_board_to_gui(decision,game.board)
          
            if(consequitive_passes == 2):
                break
            end = time.time()
            print(end - start)
    elif(game_mode == 1 ):  # AI vs AI

        
            

        game, captures, remainingTime, ourColor = READY_configuration(game)


        while ( not game.is_over()):
            if ourColor == game.next_player:
                THINKING()
            else:
                IDLE()
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
            game , captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            decision = 0
            b_time = 0
            w_time = 0
            # TODO send move to server 
            send_move_to_gui(decision,play_point,b_time,w_time,player)         
            send_board_to_gui(decision,game.board)   
            if(consequitive_passes == 2):
                break
            end = time.time()
            print(end - start)
    game_captures ={
        gotypes.Player.black : captures['0'],
        gotypes.Player.white : captures['1']
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
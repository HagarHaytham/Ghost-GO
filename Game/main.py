from dlgo.agent import naive
from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move , coords_from_point2
import interface
import copy 
from enum import Enum
from  MCTS import monte_carlo_tree_search
from dlgo.scoring import compute_game_result
import client_game as client
import time
import numpy as np
import elevenplanes
import predict
import sys
#intializations
board_size = 19
num_rounds = 10
game_mode = 0
depth = 10
consequitive_passes = 0
opponont_resigns = False

client_port = sys.argv[1] if len(sys.argv) > 1 else 7374
client_name = sys.argv[2] if len(sys.argv) > 2 else 'Ghost'
init_gui = False if len(sys.argv) > 3 else True
client.init(client_port, client_name)
if init_gui:
    interface.init()

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
        initial_state= interface.get_initial_board()
        print("initial_state >>" , len(initial_state))
        if(len(initial_state)==0):
            pass
        for i in range(0, len(initial_state)):
            point =  gotypes.Point(row= int(initial_state[i][1]),col= int(initial_state[i][0]))
            move = goboard.Move(point)
            print(">>>> move", move.point)
            game , prisoners  = game.apply_move(move)
        print(opponent)
   
    return game , captures , player , opponent

def get_player_color_from_gui():
    # print("get_player_color_from_gui")
    player = '0'
    opponent = '1'
    opponent = interface.get_opponent_color()
    print(opponent)
    if(opponent == '0'):
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
        point =  gotypes.Point(row= int(pos[1]),col= int(pos[0]))
        move = goboard.Move(point)
        # print(">>>> move", move.point)
        new_game_state , prisoners  = current_state.apply_move(move)
        captures[opponent]+=prisoners
    elif decision[0] == '1' :  # opponont_opponont_resignss
        opponont_resigns = True
    elif decision[0] == '2' : # pass
        consequitive_passes+=1
    return decision[0] , new_game_state , captures , point

def send_move_to_gui(decision,point,b_time,w_time,color,our_player='0'):
    print("send_move_to_gui")
    global consequitive_passes
    if(decision == '0'): # play
        consequitive_passes = 0 
        move = '0'+'#'+str(point.col)+'-'+str(point.row)
        print('sent point ' ,point)
    elif decision == '1': # player_resigns 
        move = '1'
    elif decision == '2': # pass
        consequitive_passes+=1
        move = '2'
    interface.send_move(move,color,str(b_time),str(w_time),our_player)
    return  

def send_board_to_gui(decision,board): 
    print("send_board_to_gui")   
    stone_list = []
    if decision == '0':
        for i in range(1,20):
            for j in range(1,20):
                stone = gotypes.Point(row= i,col= j)
                color = board.get(stone)
                if( color != None):
                    c='0'
                    if color == gotypes.Player.white :
                        c ='1'
                    stone_list.append([j,i,c])
    interface.update_board(stone_list)
    return

def send_ghost_color_to_gui(color): 
    print("send_ghost_color_to_gui")
    interface.send_ghost_color(color)

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
    interface.send_score(O_score,G_Score,reason)
    return

def READY_configuration(game):
    # Game Configuration
    response = client.handle_ready()

    if not response[0]:
        # server END message
        return False, response[1]

    parameters = response[1]
    ''' 
        Start Game configuration
    '''
    # Initial State
    for y,row in enumerate(parameters['initialState']['board']):
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

    game.next_player = gotypes.Player.black if parameters['initialState']['turn'] == 'B' else gotypes.Player.white
    # fill the board with move logs
    for logEntry in parameters['moveLog']:
        move = logEntry["move"]
        deltaTime = logEntry['deltaTime']
        if move['type'] == 'pass':
            move = goboard.Move(is_pass=True)
        elif move['type'] == 'resign':
            move = goboard.Move(is_resign=True)
        else:
            col = move['point']['column'] + 1
            row = move['point']['row'] + 1
            move = goboard.Move(gotypes.Point(row,col))

        remainingTime[game.next_player] -= deltaTime
        game,numberOfCaptures = game.apply_move(move)
        if game.next_player == gotypes.Player.white:
            captures[gotypes.Player.black] += numberOfCaptures
        else:
            captures[gotypes.Player.white] += numberOfCaptures

    ourColor = gotypes.Player.black if parameters['ourColor'] == 'B' else gotypes.Player.white
    ''' 
        End Game configuration
    '''

    return game, captures, remainingTime, ourColor

def THINKING(game, captures):
    
    played = False
    remaining_time = None
    captures = {
        '0': captures[gotypes.Player.black],
        '1': captures[gotypes.Player.white]
    }

    moves_count = 0
    while not played:
        point = -1
        player = '0' if game.next_player == gotypes.Player.black else '1'

        if moves_count == 0 or True:
            new_game , new_captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
        else:
            # another option
            pass
        decision = 0
        b_time = 0
        w_time = 0
        moves_count += 1
        
        play_move = goboard.Move(play_point)
        client.handle_thinking(play_move)

        response = client.handle_await_response()

        if not response[0]:
            # server END msg
            return False, response[1]

        if response[1]['valid']:
            played = True
            game = new_game
            captures = {
                gotypes.Player.black: new_captures['0'],
                gotypes.Player.white: new_captures['1']
            }
            remaining_time = response[1]['remaning_time']

        if not response[1]['valid']:
            reason = response[1]['message']
            print('not valid: ', reason)
            remaining_time = response[1]['remaning_time']

    # send_move_to_gui(decision,play_point,b_time,w_time,player)         
    # send_board_to_gui(decision,game.board)
    
    return game, captures, remaining_time, play_move

def IDLE(game, captures):
    response = client.handle_idle()
    if not response[0]:
        # server END msg
        return False, response[1]

    if response[1]['type'] == 'place':
        point = gotypes.Point(response[1]['row'] + 1, response[1]['column'] + 1)
        move = goboard.Move(point)
    elif response[1]['type'] == 'pass':
        move = goboard.Move(is_pass = True)
    elif response[1]['type'] == 'resign':
        move = goboard.Move(is_resign = True)
    
    game, prisoners = game.apply_move(move)
    captures[game.next_player.other] += prisoners

    return game, captures, response[1]['remaning_time'], move

def AI_vs_AI():
    while True:
        while not client.connected:
            response = client.handle_init()

        game = goboard.GameState.new_game(board_size)
        response = READY_configuration(game)
        if response is not False:
            game, captures, remainingTime, ourColor = response
            if init_gui:
                send_board_to_gui(0, game.board)
                send_ghost_color_to_gui('0' if ourColor == gotypes.Player.black else '1')
            our_player = '0' if ourColor == gotypes.Player.black else '1'

            while not game.is_over():
                print_board(game.board)
                old_captures = copy.copy(captures)
                if game.next_player == ourColor:
                    response = THINKING(game, captures)
                    if response[0] is False:
                        # server END message
                        break
                    else:
                        game, captures, remainingTime, play_move = response
                else:
                    response = IDLE(game, captures)
                    if response[0] is False:
                        # server END message
                        break
                    else:
                        game, captures, remainingTime, play_move = response

                # update the gui
                if init_gui:
                    if captures[game.next_player.other] != old_captures[game.next_player.other]:
                        send_board_to_gui(0, game.board)
                    else:
                        decision = 0
                        decision = 1 if play_move.is_resign else decision
                        decision = 2 if play_move.is_pass else decision
                        player = '0' if game.next_player.other == gotypes.Player.black else '1'
                        send_move_to_gui(decision, play_move.point, remainingTime['B'], remainingTime['W'], player, our_player)


        result = response[1]
        print(result)
        game_result,score = game.winner(captures)
        print(game_result, score)
        game_result = (result['B_score'], result['B_score'])
        reason = result['reason']
        if init_gui:
            send_score_to_gui(game_result,our_player,reason)
        time.sleep(5)
            
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
    # print('in main',new_point)
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
    if(O_score1==O_score2): 
        return "equal"
    elif(O_score1 > O_score2 ):
        return "gt"
    return "lt"
def send_congrats():
    congrats_msg ='Nice Move !!'
    interface.send_congrate(congrats_msg)
def send_recommended_move(decision,point):
    msg = str(decision)
    if(decision ==0):
        msg = msg+'#'+str(point.col)+'-'+str(point.row)
    else:
        msg = msg+'#0'
    print("Recommended Move in sendRecmove Func : ",msg)    
    interface.send_recommended_move(msg)

def main():
    global consequitive_passes, opponont_resigns, game_mode
    if init_gui:
        game, captures, player, opponent = get_game_mode_from_gui()
        first_game = False

        if( opponent == "1"):
            first_game = True
        print('first',first_game)
    else:
        game_mode = 1
    
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
                print("Recommended Move is : ",recommended_move)
                if(result == "gt"):
                    print("Send Recommended move condition in main")
                    send_recommended_move(decision,recommended_move)
                    pass
                else: 
                    send_congrats()
                    pass
                print("captures[opponent] old_captures : ", captures[opponent], old_captures)
                if( captures[opponent] > old_captures):
                    print('opponent captures')
                    send_board_to_gui(decision,game.board)      
                b_time = 0
                w_time = 0
                if(consequitive_passes == 2 or opponont_resigns == True ):
                    break
            
            old_captures = copy.copy(captures[player])
            game , captures , play_point = monte_carlo_tree_search( game,point,player,num_rounds,captures,depth)
            print('after monto carlo')
            decision = '0'
            b_time = '0'
            w_time = '0'
            send_move_to_gui(decision,play_point,b_time,w_time,player)  
            if(captures[player] > old_captures):
                print('player captures')
                send_board_to_gui(decision,game.board)
            first_game = False
            if(consequitive_passes == 2):
                break
            end = time.time()
            # print(end - start)

        game_captures ={
            gotypes.Player.black : captures['0'],
            gotypes.Player.white : captures['1']
        }
        #game_result,winner,score = game.winner(game_captures)
        game_result,score = game.winner(game_captures)
        reason = 'IDK!'
        send_score_to_gui(game_result,player,reason)
        # if winner == '0':
        #     print("Black is the WINNER!!!!")
        # else:
        #     print("White is the WINNER!!!!")

        # print('Black:', score[gotypes.Player.black] ,'\tWhite:', score[gotypes.Player.white])
    elif(game_mode == 1 ):  # AI vs AI
        AI_vs_AI()
    

if __name__ == '__main__':
    main()
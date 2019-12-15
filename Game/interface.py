import zmq
import threading

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)
pull_socket = context.socket(zmq.PULL)

def init():    
    global push_socket, pull_socket
    push_socket.bind("tcp://127.0.0.1:3001")
    pull_socket.connect("tcp://127.0.0.1:3000")

def get_game_mode():
    while(True):
        game_mode = pull_socket.recv()
        # if game_mode != 0:
        return game_mode #.decode('utf-8')
    
def get_opponent_color():
    while(True):
        opponent_color = pull_socket.recv()
        # if opponent_color != 0:
        opponent_color = opponent_color.decode('utf-8')
        return opponent_color

def get_opponent_move(): #till now it blocks, in case computations are needed at this time, open a thread
    while(True):
        opponent_move = pull_socket.recv()
        print("opponent_move : ",opponent_move)
        # if opponent_move != 0:
        opponent_move = opponent_move.decode('utf-8')
        return opponent_move

def get_initial_board():
    while(True):
        initial_board = pull_socket.recv()
        print("intefaace.py",initial_board)
        # if initial_board != 0:
        stones = []
        if(initial_board.decode('utf-8') == '1'): 
            with open('initial_state.txt') as f:
                f.seek(0)
                first_char = f.read(1) #get the first character
                while not first_char:
                    f.seek(0)
                    first_char = f.read(1)
                    # print("empty")
                f.seek(0)
                comp_stones = f.read().splitlines()
                # print("comp_stones >> ", comp_stones)
                for s in comp_stones:
                    stones.append(s.split('-'))
                f.close()  
        return stones # 2D list each record --> col, row, color ALL are strings  /// [] if empty

def send_ghost_color(color):
    c = 'COLOR,' + color
    push_socket.send_string(c)

def send_move(move, color, B_time, W_time,our_player):
    if our_player == '0':
        time = W_time + '#' + B_time
    else:
        time = B_time + '#' + W_time  
    m = 'MOVE,' + move + '#' + color + '#' + time
    push_socket.send_string(m)

def send_state(state):
    s = 'STATE'
    #write state in file
    f = open("send_state.txt",'w')
    for i in range (len(state)):
        f.write(str(state[i][0])+',')
        f.write(str(state[i][1])+',')
        f.write(str(state[i][2])+',')
    push_socket.send_string(s)

def update_board(state):
    if state == []:
        return
    s = 'UPDATE'
    #write state in file
    f = open("update_board.txt",'w')
    for i in range (len(state)):
        f.write(str(state[i][0])+',')  #x
        f.write(str(state[i][1])+',')   #y
        f.write(str(state[i][2])+',')   #color
    f.close()
    print("Hi")
    push_socket.send_string(s)
    print("Bye")

def send_valid_moves(vaild_moves):
    print(len(vaild_moves))
    v = 'VALID'
    f = open("valid_moves.txt",'w')
    for i in range (len(vaild_moves)):
        # print(vaild_moves[i][0],vaild_moves[i][1])
        f.write(str(vaild_moves[i][0])+',') #x
        f.write(str(vaild_moves[i][1])+',') #y
    f.close()
    push_socket.send_string(v)

def send_score(O_score, G_score, reason):
    s = 'SCORE,' + O_score + '#' + G_score + '#' + reason
    push_socket.send_string(s)
    # push_socket.close()
    # pull_socket.close()

def send_recommended_move(move):
    m = 'REC_MOVE,' + move
    print("Recommended Move in Interface : ",move) 
    push_socket.send_string(m)

def send_congrate(msg): 
    g = 'CONGRATULATE,' + msg
    push_socket.send_string(g)

import zmq
import threading

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)
pull_socket = context.socket(zmq.PULL)

push_socket.bind("tcp://127.0.0.1:3001")
pull_socket.connect("tcp://127.0.0.1:3000")


def get_game_mode():
    while(True):
        game_mode = pull_socket.recv()
        if game_mode != 0:
            return game_mode
    
def get_opponent_color():
    while(True):
        opponent_color = pull_socket.recv()
        if opponent_color != 0:
            return opponent_color

def get_opponent_move(): #till now it blocks, in case computations are needed at this time, open a thread
    while(True):
        opponent_move = pull_socket.recv()
        print(opponent_move)
        if opponent_move != 0:
            return opponent_move
    
def send_move(move, color, O_time, G_time):
    m = 'MOVE,' + move + '#' + color + '#' + O_time + '#' + O_time
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
    s = 'UPDATE'
    #write state in file
    f = open("update_board.txt",'w')
    for i in range (len(state)):
        f.write(str(state[i][0])+',')  #x
        f.write(str(state[i][1])+',')   #y
        f.write(str(state[i][2])+',')   #color
    push_socket.send_string(s)

def send_valid_moves(vaild_moves):
    v = 'VALID'
    f = open("valid_moves.txt",'w')
    for i in range (len(vaild_moves)):
        print(vaild_moves[i][0],vaild_moves[i][1])
        f.write(str(vaild_moves[i][0])+',') #x
        f.write(str(vaild_moves[i][1])+',') #y
    push_socket.send_string(v)

def send_score(O_score, G_score, reason):
    s = 'SCORE,' + O_score + '#' + G_score + '#' + reason
    push_socket.send_string(s)

def send_recommended_move(move):
    m = 'REC_MOVE,' + move
    push_socket.send_string(m)

def send_congrate(msg): 
    m = 'CONGRATULATE,' + msg
    push_socket.send_string(m)

state = [[1,2,'1'],[3,4,'0'],[5,6,'1']]
send_state(state)
# get_opponent_move()
# send_state("starting_state")

import zmq
import threading

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)
pull_socket = context.socket(zmq.PULL)

push_socket.bind("tcp://127.0.0.1:3001")
pull_socket.connect("tcp://127.0.0.1:3000")


def get_game_mode():
    print("getting game mode ..")
    while(True):
        game_mode = pull_socket.recv()
        if game_mode != 0:
            print("recieving game_mode >> ", game_mode)
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

def send_state(state): ##
    s = 'STATE,'+state
    push_socket.send_string(s)

def send_valid_moves(vaild_moves): ##
    v = 'VALID,' + vaild_moves
    t = threading.Thread(target=send_moves, args=(v,))
    t.start()

def send_moves(v):
    print("thread starts with v = ",v)
    push_socket.send_string(v)

def send_ghost_move(move):
    m = 'MOVE,' + move
    push_socket.send_string(m)
    
def send_move(move, color):
    m = 'MOVE_COLOR,' + move + ',' + color
    push_socket.send_string(m)

def send_score(game_mode, score1, score2='0'): #score2 for AI mode
    s = 'SCORE,' + score1
    if game_mode == '0': #AI Mode
        s += '-' + score2
    push_socket.send_string(s)
    print("score was sent", s)

def send_recommended_move(move):
    m = 'REC_MOVE,' + move
    push_socket.send_string(m)

def send_congrate(msg): 
    m = 'CONGRATULATE,' + msg
    push_socket.send_string(m)

get_opponent_move()
send_state("starting_state")

import zmq
import threading

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)
pull_socket = context.socket(zmq.PULL)

push_socket.bind("tcp://127.0.0.1:3001") #tcp://127.0.0.1:3000  #bind("tcp://127.0.0.1:3001") #tcp://127.0.0.1:3001
pull_socket.connect("tcp://127.0.0.1:3000") #tcp://127.0.0.1:3001 #connect("tcp://192.168.37.11:3000") #tcp://127.0.0.1:3000


#giving codes to different messages.
#

def get_game_mode():
    print("getting game mode ..")
    while(True):
        game_mode = pull_socket.recv()
        print("waiting")
        if game_mode != 0:
            print("recieving game_mode >> ", game_mode)
            return game_mode
        print("do not recievig, do not blocking")
    
def get_oppenent_color():
    while(True):
        oppenent_color = pull_socket.recv()
        if oppenent_color != 0:
            return oppenent_color

def send_state(state):
    # t = threading.Thread(target=send_moves, args=('t1',10,))
    # t.start()
    push_socket.send(state)

def send_valid_moves(vaild_moves):
    t = threading.Thread(target=send_moves, args=('t1',10,))
    t.start()
def send_moves():
    push_socket.send(vaild_moves)

def send_ghost_move(move):
    push_socket.send(move)
    #get_oppenent_move
    while(True):
        oppenent_move = pull_socket.recv()
        if oppenent_move != 0:
            return oppenent_move

def send_score(score):
    print("try to send score")
    push_socket.send_string(score)
    print("sended")




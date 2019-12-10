import zmq
import threading

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)
pull_socket = context.socket(zmq.PULL)

push_socket.bind("tcp://127.0.0.1:3001")
pull_socket.connect("tcp://127.0.0.1:3000")


t = threading.Thread(target=send_moves, args=(v,))
t.start()
while(True):
    # state = enum["READY","THINKING","AWAITING_MOVE_RESPONSE","IDLE","END"]
    state = pull_socket.recv()
    if state == "0":

    elif state == "1":
        
    elif state == "2":

    elif state == "3":
        
    elif state == "4":
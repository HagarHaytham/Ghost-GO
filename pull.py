import zmq

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket2 = context.socket(zmq.PULL)

socket.bind("tcp://127.0.0.1:3001")
socket2.connect("tcp://127.0.0.1:3000")

while(True):
    message = 0 
    message = socket2.recv()
    if (message != 0):
        print("Received request: %s" % message)
    print("Sending Hello ")
    socket.send(b"Hello")

import zmq
import random
import sys
import time

port = "3001"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:3001")
while True:
    topic = "hello"
    messagedata = "world"
    print ("%s %s"%(topic, messagedata))
    socket.send_string("%s %s"%(topic, messagedata))
    time.sleep(1)
import zmq
import subprocess
import atexit

context = client_socket = None
connected = False

def init(port=7374, name='Ghost'):
    global context, client_socket

    context = zmq.Context()
    #  Socket to talk to server
    client_socket = context.socket(zmq.REQ)
    client_socket.connect("tcp://localhost:" + str(port))
    
    client_process = subprocess.Popen("python client.py " + str(port) + ' ' + name)

    def exit_handler():
        client_process.kill()

    atexit.register(exit_handler)

def handle_init():
    global connected
    # print("init")
    response = send_to_client({})
    connected = response[0]
    return response

def handle_ready():
    # print("ready")
    return send_to_client({})

def handle_thinking(move):
    # print("thinking")
    # print('thinking', move.point)
    move_type = 'place'
    move_type = 'pass' if move.is_pass else move_type
    move_type = 'resign' if move.is_resign else move_type
    
    move_payload = {"type": move_type}
    if move_type == 'place':
        move_payload["point"] = {'row': int(move.point.row - 1), 'column': int(move.point.col) - 1}

    parameters = {
        'move': move_payload
    }
    return send_to_client(parameters)

def handle_await_response():
    # print("await_response")
    return send_to_client({})

def handle_idle():
    # print("idle")
    return send_to_client({})

def send_to_client(parameters):
    global connected
    # print('send')
    client_socket.send_json(parameters)
    #  Get the reply.
    message = client_socket.recv_json()
    # print(message)
    success = message[0]
    connected = message[1]
    payload = message[2]
    return success, payload
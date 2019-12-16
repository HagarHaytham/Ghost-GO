import websockets
import asyncio
import json
from time import sleep
from threading import Thread
import zmq
import atexit
import sys
import concurrent.futures


async def blocking_to_async(func, *args):
    result = await asyncio.wait(fs={
        asyncio.get_event_loop().run_in_executor(
            concurrent.futures.ThreadPoolExecutor(1),
            func, *args
        )
    })
    return_val = tuple(element.result() for element in tuple(result[0]))
    # print(return_val)
    return return_val[0] if len(return_val) == 1 else return_val

context = game_engine_socket = None
states = {
    "INIT": 0,
    "READY": 1,
    "THINKING": 2,
    "AWAIT_MV_RES": 3,
    "IDLE": 4
}

name = "Ghost"
url = "ws://localhost:8080"

websocket = None
current_state = states["INIT"]

restart = False
connected = False




async def handle_init():
    global websocket, current_state, connected
    websocket = await websockets.connect(url, ping_interval=None)  # connect to server
    connected = True
    msg = await websocket.recv()
    msg = json.loads(msg)
    if msg["type"].lower() == "name":
        msg = json.dumps({"type": "NAME", "name": name})
        await websocket.send(msg)
        current_state = states["READY"]
        return
    elif msg["type"] == "END":
        return handle_end(msg)


async def handle_ready():
    global current_state, websocket
    # print("now handling ready")
    msg = await websocket.recv()
    # print("received", msg)
    msg = json.loads(msg)
    if msg["type"] == "START":

        initialState = msg['configuration']['initialState']
        moveLog = msg['configuration']['moveLog']
        color = msg["configuration"]["initialState"]["turn"]

        if msg["color"] == initialState['turn'] and len(moveLog) % 2 == 0 or msg["color"] != initialState['turn'] and len(moveLog) % 2 != 0:
            current_state = states['THINKING']
        else:
            current_state = states['IDLE']

        parameters = {
            "initialState":initialState,
            "moveLog":moveLog,
            "ourColor":msg["color"]
        }

        return parameters

    elif msg["type"] == "END":
        return handle_end(msg)


def handle_end(msg):
    global current_state, restart
    restart = True
    # print("END GAME reason is "+ msg['reason'])
    score = {
        'reason': msg['reason'],
        'winner': msg['winner'],
        'B_score': msg['players']["B"]["score"],
        'B_remaining_time': msg['players']["B"]["remainingTime"],
        'W_score': msg['players']["W"]["score"],
        'W_remaining_time': msg['players']["W"]["remainingTime"]
    }


    current_state = states["READY"]
    return score


async def handle_thinking(parameters):
    global current_state, websocket

    move = parameters['move']
    msg = {"type": "MOVE", "move": move}

    msg = json.dumps(msg)
    await websocket.send(msg)
    current_state = states["AWAIT_MV_RES"]

    return


async def handle_await_response():
    global current_state, websocket
    msg = await websocket.recv()
    msg = json.loads(msg)
    # print(msg)
    if msg["type"] == "VALID":
        current_state = states["IDLE"]
        return { 'valid': True, 'remaning_time': msg["remainingTime"] }
    elif msg["type"] == "INVALID":
        current_state = states["THINKING"]
        return { 'valid': False, 'remaning_time': msg["remainingTime"], 'message': msg["message"] }
    elif msg["type"] == "END":
        return handle_end(msg)


async def handle_idle():
    global current_state, websocket
    msg = await websocket.recv()
    msg = json.loads(msg)
    if msg["type"] == "MOVE":
        current_state = states["THINKING"]
        if msg["move"]["type"] == "place":
            return {
                'type': msg["move"]["type"],
                'row': msg["move"]["point"]["row"],
                'column': msg["move"]["point"]["column"],
                'remaning_time': msg["remainingTime"]
            }
        else:
            return {
                'type': msg["move"]["type"],
                'remaning_time': msg["remainingTime"]
            }
    elif msg["type"] == "END":
        return handle_end(msg)


async def main():
    global current_state, restart, connected
    while True:
        #  Wait for game engine request
        message = await blocking_to_async(game_engine_socket.recv_json)
        #  = game_engine_socket.recv_json()
        print('send', message)
        return_value = None
        # print("State: " + str(current_state), message)
        try:
            if current_state == states["INIT"]:
                return_value = await handle_init()
            elif current_state == states["READY"]:
                return_value = await handle_ready()
            elif current_state == states["THINKING"]:
                return_value = await handle_thinking(message)
            elif current_state == states["AWAIT_MV_RES"]:
                return_value = await handle_await_response()
            elif current_state == states["IDLE"]:
                return_value = await handle_idle()
        except Exception as e:
            connected = False
            restart = True
            # print("type error: " + str(e))
            current_state = states["INIT"]

        print('received', return_value, (not restart), connected)
        message = (not restart), connected, return_value
        #  Send reply back to the game engine
        game_engine_socket.send_json(message)
        restart = False



async def ping_pong():
    global websocket
    while True:
        try:
            await websocket.pong()
            await asyncio.sleep(0.5)
            # # print("ping")
        except Exception as e:
            pass
            # # print(f"ping pong exception {str(e)}")

def pong():
    asyncio.run(ping_pong())


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else url
    port = sys.argv[2] if len(sys.argv) > 2 else 7374
    name = sys.argv[3] if len(sys.argv) > 3 else 'Ghost'
    
    context = zmq.Context()
    game_engine_socket = context.socket(zmq.REP)
    game_engine_socket.bind("tcp://*:" + str(port))

    asyncio.run(main())
    # Thread(target=pong).start()  # ping pong

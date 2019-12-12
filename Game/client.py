import websockets
import asyncio
import json
from time import sleep
from threading import Thread

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
my_color = None
current_state = states["INIT"]


def gameState(state, msg=''):
	pass

async def dummy():
    await asyncio.sleep(2)
    return {"type": "pass"}


def send_valid(valid, remaning_time, message=""):
    pass


def send_opponent_move(type, X, Y, time):
    pass


def send_score(reason, winner, B_score, B_time, W_score, W_time):
    pass


async def ping_pong():
    global websocket
    while True:
        try:
            await websocket.send()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"ping pong exception {str(e)}")


async def handle_init():
    global websocket, current_state
    websocket = await websockets.connect(url, ping_interval=None)  # connect to server
    msg = await websocket.recv()
    msg = json.loads(msg)
    if msg["type"].lower() == "name":
        msg = json.dumps({"type": "NAME", "name": name})
        await websocket.send(msg)
        current_state = states["READY"]
    elif msg["type"] == "END":
        return handle_end(msg)
    return None


async def handle_ready():
    global current_state, my_color, websocket
    print("now handling ready")
    msg = await websocket.recv()
    print("received", msg)
    msg = json.loads(msg)
    if msg["type"] == "START":
        color = msg["configuration"]["initialState"]["turn"]
        log_entries = []
        for log_entry in msg["configuration"]["moveLog"]:
            entry = {"type": log_entry["move"]["type"], "color": color}
            if entry["type"] == "place":
                entry["point"] = log_entry["move"]["point"]
            log_entries.append(entry)
            color = "B" if color == "W" else "W"
        log_entries = [x for x in log_entries if x["type"] != "pass"]
        if (msg["color"] == msg["configuration"]["initialState"]["turn"] and len(msg["configuration"]["moveLog"]) % 2 == 0) or (msg["color"] != msg["configuration"]["initialState"]["turn"] and len(msg["configuration"]["moveLog"]) % 2 != 0):
            # TODO: send to integration the color, log_entry and initial_state
            current_state = states["THINKING"]
            my_color = msg["color"]
        else:
            current_state = states["IDLE"]
            my_color = "B" if msg["color"] == "W" else "W"
    elif msg["type"] == "END":
        handle_end(msg)


def handle_end(msg):
    global current_state
    print("END GAME reason is "+ msg['reason'])
    send_score(reason=msg['reason'], winner=msg['winner'], B_score=msg['players']["B"]["score"], B_time=msg['players']
               ["B"]["remainingTime"], W_score=msg['players']["W"]["score"], W_time=msg['players']["W"]["remainingTime"])
    current_state = states["READY"]


async def handle_thinking():
    global current_state, websocket
    move = await dummy()  # call thinking logic
    msg = {"type": "MOVE", "move": {"type": move["type"]}}
    if move["type"] == "place":
        msg["move"]["point"] = {"row": move["X"], "column": move["Y"]}
    msg = json.dumps(msg)
    await websocket.send(msg)
    current_state = states["AWAIT_MV_RES"]


async def handle_await_response():
    global current_state, websocket
    msg = await websocket.recv()
    msg = json.loads(msg)
    if msg["type"] == "VALID":
        send_valid(valid=True, remaning_time=msg["remainingTime"][my_color])
        current_state = states["IDLE"]
    elif msg["type"] == "INVALID":
        send_valid(
            valid=False, remaning_time=msg["remainingTime"][my_color], message=msg["message"])
        current_state = states["THINKING"]
    elif msg["type"] == "END":
        handle_end(msg)


async def handle_idle():
    global current_state, websocket
    msg = await websocket.recv()
    msg = json.loads(msg)
    if msg["type"] == "MOVE":
        if msg["move"]["type"] == "place":
            send_opponent_move(type=msg["move"]["type"], X=msg["move"]["point"]["row"],
                               Y=msg["move"]["point"]["column"], time=msg["remainingTime"][my_color])
        else:
            send_opponent_move(
                type=msg["move"]["type"], X=0, Y=0, time=msg["remainingTime"][my_color])
        current_state = states["THINKING"]
    elif msg["type"] == "END":
        handle_end(msg)


async def main():
    global current_state
    while True:
        try:
            if current_state == states["INIT"]:
                await handle_init()
            elif current_state == states["READY"]:
                await handle_ready()
            elif current_state == states["THINKING"]:
                await handle_thinking()
            elif current_state == states["AWAIT_MV_RES"]:
                await handle_await_response()
            elif current_state == states["IDLE"]:
                await handle_idle()
        except Exception as e:
            print("type error: " + str(e))
            current_state = states["INIT"]


if __name__ == "__main__":
    asyncio.run(main())
    Thread(target=ping_pong).start()  # ping pong

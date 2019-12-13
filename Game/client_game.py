import main 
import client

def get_state_from_client():
    state,parameters = client.send_state()
    if state == 1:  # Ready
        # Parameters ={
        #  "gameConfiguration": {
            #  "initialState": GameState,
            #  "moveLog": [LogEntry],
            #  "komi":number,
            #  "ko": boolean,
            #  "scoringMethod": string,
            #  "prisonerScore": number,
            #  "idleDeltaTime": Time
        #   },
        #   "color": Color
        # } 
        initialState = parameters['gameConfiguration']['initialState']
        moveLog = parameters['gameConfiguration']['moveLog']
        color = parameters['color']
        
        parameters = {
            "initialState":initialState,
            "moveLog":moveLog,
            "ourColor":color
        }
    elif state == 2:# Thinking
        move = main.send_move_to_client()
        if move.is_pass:
            move_str = 'passes'
        elif move.is_resign:
            move_str = 'resigns'

        parameters = {
            "type":move_str,
            "X":move.point.col,
            "Y":move.point.row
        }
        # communication.get_move(parameters)
    elif state == 3:# Awaiting Move Response
        # parameters = {
        #     valid: Boolean,
        #     remaining_time: int,
        #     message: string
        # }
        # main.get_vaild(parameters)
        pass
    elif state == 4:# Idel
        # Parameters = {
        #   "type" : string,
        #   "X" : int,
        #   "Y": int,
        #   "time": int
        # }
        # main.send_opponent_move(parameters)
        pass
    return parameters

def get_move_from_game(move):
    move_str = 'place'
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'

    parameters = {
        "type":move_str,
        "X":move.point.col if move_str == 'place' else None,
        "Y":move.point.row  if move_str == 'place' else None
    }

def get_parameters_from_client_game():
    parameters = get_state_from_client()
    return parameters
import main 
import communication

def get_state_from_client():
    state,parameters = communication.send_state()
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
        idelDeltaTime = parameters['gameConfiguration']["idleDeltaTime"]
        color = parameters['color']
        turn = parameters['turn']
        parameters = {
            "initialState":initialState,
            "moveLog":moveLog,
            "idleDeltaTime": idelDeltaTime,
            "turn": turn
        }
        main.get_game_configuration(parameters)
    elif state == 2:# Thinking
        move = main.get_move()
        if move.is_pass:
            move_str = 'passes'
        elif move.is_resign:
            move_str = 'resigns'

        parameters = {
            "type":move_str,
            "X":move.point.col,
            "Y":move.point.row
        }
        communication.get_move(parameters)
    elif state == 3:# Awaiting Move Response
        # parameters = {
        #     valid: Boolean,
        #     remaining_time: int,
        #     message: string
        # }
        main.get_vaild(parameters)
    elif state == 4:# Idel
        # Parameters = {
        #   "type" : string,
        #   "X" : int,
        #   "Y": int,
        #   "time": int
        # }
        main.send_opponent_move(parameters)
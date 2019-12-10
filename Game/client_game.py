import main
import communication

def get_state_from_client(){
    state = communication.send_state()
    if state == 1:  # Ready
        pass
    elif state == 2:# 
        pass
    elif state == 3:# 
        pass
    elif stata == 4:# 
        pass
}

def send_state_to_game_engine(state,parameters){
    main.get_state(state,parameters)
}
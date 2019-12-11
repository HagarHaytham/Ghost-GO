'''

1. Get the game mode from GUI

2. Depending on the game mode 
    IF Human vs Bot : get the colors from the GUI
    IF Bot vs Bot   : listen to the server 

3. Depending on the game mode
    IF Human vs Bot : Get the human and bot moves and change the GUI immediately
    IF Bot vs Bot   : Listen to the server and get states

4. In Bot vs Bot mode
    If state == "0" : Get the color and initial state from the server and pass it to the GUI
    If state == "1" : Let our agent choose a valid move and send it back to the server (don't change the GUI)
    If state == "2" : Get the validation of the move played (supposed to be True) , applied move#remaining time (pass it to the GUI) 
    If state == "3" : Get the oponent move and apply it to the board and change the GUI immediately
    If state == "4" : Get the score of the ended game pass (the score, the winner, time for each player) to GUI 

'''
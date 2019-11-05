var zmq = require("zeromq");
to_game = zmq.socket("push");
from_game = zmq.socket("pull");
var oppo_mode = 0;
var state = 1;
to_game.bindSync("tcp://127.0.0.1:3000");
from_game.connect("tcp://127.0.0.1:3001");

console.log("GUI interface started!");

//TO-DO : ADD SWITCH CASE.
//TO-DO : REPLACE PLACE HOLDERS. 
from_game.on("message", function(msg) {

    console.log("work from pull: %s", msg.toString());
    result = msg.toString();
    l = result.split(',');
    console.log(l[0])

    if (l[0] == 'STATE') draw_state(l[1]);
    else if(l[0] == 'VALID') show_moves(l[1]);
    else if(l[0] == 'MOVE')  draw_move(l[1]);
    else if(l[0] == 'SCORE') show_score(l[1]);
    else console.log("invalid message code.")
});

// to start, we should know our opponent to decide on the methods used later.
function send_mode(mode){
    to_game.send(mode);
    oppo_mode = mode; 
}

function draw_state(state)
{
    console.log('Drawing a state.');
}

function draw_move(move)
{
    console.log('Making a move.');
}

function show_score(score)
{
    console.log('SCORE!');
}


// white : 1 , black : 0
function send_opponent_color(color){
    to_game.send(color);
}

function send_opponent_move(move){
    to_game.send(move);
    return true;
}




var zmq = require("zeromq");
to_game = zmq.socket("push");
from_game = zmq.socket("pull");
to_game.bindSync("tcp://127.0.0.1:3000");
from_game.connect("tcp://127.0.0.1:3001");

console.log("GUI interface started!");
var oppo_mode = 0;
var state = 1;

//TO-DO : REPLACE PLACE HOLDERS. 
from_game.on("message", function(msg) {

    // console.log("work from pull: %s", msg.toString());
    result = msg.toString();
    l = result.split(',');
    
    switch(l[0]){
        case 'STATE':
            draw_state(l[1]);
            break;
        case 'VALID':
            draw_moves(l[1]);
            break;
        case 'MOVE':
            draw_move(l[1]);
            break;
        case 'SCORE':
            show_score(l[1]);
            break;
        default:
            console.log("invalid message code from implementation side.")
    }
});

// to start, we should know our opponent to decide on the methods used later.
function send_mode(mode){
    to_game.send(mode);
    oppo_mode = mode; 
}

function draw_state(state)
{
    console.log('Drawing a state.');
    // your code goes here
}

function draw_move(move)
{
    console.log('Making a move.');
    // your code goes here
}

function draw_moves(moves)
{
    console.log('Draw possible moves.');
    // your code goes here
}

function show_score(score)
{
    console.log('SCORE!');
    console.log(score);
    // your code goes here
}

// white : 1 , black : 0
function send_opponent_color(color){
    to_game.send(color);
}

function send_opponent_move(move){
    to_game.send(move);
    return true;
}

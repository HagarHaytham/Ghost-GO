var zmq = require("zeromq");
var to_game = zmq.socket("push");
to_game.bindSync("tcp://127.0.0.1:3000");



console.log("GUI interface started!");
var oppo_mode = 0;

// white : 1 , black : 0
function send_opponent_color(color){
    console.log("interface: color: ", color)
    to_game.send(color);
}

function send_opponent_move(move_type, position){
    to_game.send(move_type+"#"+position);
}


// to start, we should know our opponent to decide on the methods used later.
function send_mode(mode){
    to_game.send(mode);
    oppo_mode = mode; 
}


module.exports = {send_mode, send_opponent_color, send_opponent_move};
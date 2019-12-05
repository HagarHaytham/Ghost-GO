var zmq = require("zeromq");
to_game = zmq.socket("push");
from_game = zmq.socket("pull");
to_game.bindSync("tcp://127.0.0.1:3000");
from_game.connect("tcp://127.0.0.1:3001");

console.log("GUI interface started!");
var game_mode = 0;
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
        case 'CONGRATULATE':
            congratulate(l[1]);
            break;
        case 'MOVE_COLOR':
            draw_move_color(l[1],l[2]);
            break;
        case 'REC_MOVE':
            show_recommended_move(l[1]);
            break;
        default:
            console.log("invalid message code from implementation side.")
            break;
    }
});

// to start, we should know our opponent to decide on the methods used later.

function draw_state(state)
{
    console.log('Drawing a state.');
    console.log(state)
}

function draw_move(move)
{
    console.log('GHOST MOVE: ');
    console.log(move)
}

function draw_move_color(move,color)
{
    console.log('AI MOVE: '+move+' '+color);
}


function show_score(score)
{
    console.log('SCORE: '+score);
    /*
    if(game_mode == '0')
        scores = score.split('-');
        console.log("ME: "+scores[0]",OTHER: "+scores[1]);
    e
    */
    
}

function congratulate(msg)
{
    console.log('CONGRATS:');
    console.log(msg)

}
function draw_moves(moves) // to draw valid moves.
{
    console.log('Draw valid moves.');
    console.log(moves)
}

function show_recommended_move(move) // in addition to valid moves, There can be a specific recommended move.
{

    console.log('Recommended Moves:'+ move);
}

// white : 1 , black : 0
function send_opponent_color(color){
    to_game.send(color);
}


function send_opponent_move(move_type,position,time){
    to_game.send(move_type+"#"+position+"#"+time);
}
function send_mode(mode){
    to_game.send(mode);
    oppo_mode = mode; 
}

send_opponent_move('0','B-12','1');

const guiIndex = require("../js/index.js");
const guiScore = require("../js/index.js");
var zmq = require("zeromq");
var from_game = zmq.socket("pull");
from_game.connect("tcp://127.0.0.1:3001");
console.log("GUI from game interface started!");
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


function draw_state(state)
{
    console.log('Drawing a state.');
    // your code goes here
}

function draw_move(move)
{
    console.log('Making a move.');
    // your code goes here
    guiIndex.drawMove(move);
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
    guiScore.showScore(score);
    // your code goes here
}




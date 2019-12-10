var zmq = require("zeromq");
var fs = require('fs');
to_game = zmq.socket("push");
from_game = zmq.socket("pull");
to_game.bindSync("tcp://127.0.0.1:3000");
from_game.connect("tcp://127.0.0.1:3001");

console.log("GUI interface started!");
var game_mode = 0;


//TO-DO : REPLACE PLACE HOLDERS. 
from_game.on("message", function(msg) {

    // console.log("work from pull: %s", msg.toString());
    result = msg.toString();
    l = result.split(',');
    
    switch(l[0]){
            case 'STATE':
            draw_state('send_state.txt');
            break;
        case 'VALID':
            draw_moves('valid_moves.txt');
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
        case 'REC_MOVE':
            show_recommended_move(l[1]);
            break;
        case 'UPDATE':
            update_board('update_board.txt');
            break;
        case 'COLOR':
            get_ghost_color(l[1]);
            break;
        default:
            console.log("invalid message code from implementation side.")
            break;
    }
});

// to start, we should know our opponent to decide on the methods used later.

function draw_state(file_name)
{
    fs.readFile(file_name, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            console.log('received data: ' + data);
            var tmp = data.split(',');
            var stone_count = (tmp.length-1)/3;
            var state = new Array(stone_count);
            for(i = 0 ; i<stone_count;i++)
            {
                state[i] = new Array(3);
                for(j = 3*i ; j<3*i+3; j++)
                {
                    state[i][j%3] = parseInt(tmp[j], 10);  
                    console.log(tmp[j]);
                }
            }
            //call gui function here. each row contains x,y,color.
        } else {
            console.log(err);
        }
    })    
}
function draw_moves(moves) // to draw valid moves.
{
    fs.readFile(file_name, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            console.log('received data: ' + data);
            var tmp = data.split(',');
            var stone_count = (tmp.length-1)/2;
            var valid = new Array(stone_count);
            for(i = 0 ; i<stone_count;i++)
            {
                valid[i] = new Array(2);
                for(j = 2*i ; j<2*i+2; j++)
                {
                    valid[i][j%2] = parseInt(tmp[j], 10);  
                    console.log(tmp[j]);
                }
            }
            //call gui function here. each row contains x,y.
        } else {
            console.log(err);
        }
    })
    
}
function draw_move(move)
{
    var tmp_move = move.split('#')
    //tmp_move[0] : move type
    //tmp_move[1] : coordinates.
    //tmp_mover[2] : color
    //tmp_move[3] :O-time  -- black time.
    //tmp_move[4] :G-time  -- white time.
    var tmp_coord = tmp_move[1].split('-');
    //tmp_coord[0] : x , tmp_coord[1] = y.
    
    //gui_func()
    
}



function update_board(file_name)
{
    fs.readFile(file_name, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            console.log('received data: ' + data);
            var tmp = data.split(',');
            var stone_count = (tmp.length-1)/3;
            var state = new Array(stone_count);
            for(i = 0 ; i<stone_count;i++)
            {
                state[i] = new Array(3);
                for(j = 3*i ; j<3*i+3; j++)
                {
                    state[i][j%3] = parseInt(tmp[j], 10);  
                    console.log(tmp[j]);
                }
            }
            //call gui function here. each row contains x,y,color.
        } else {
            console.log(err);
        }
    })    
}


function show_score(score)
{
    console.log('SCORE: '+score);
    var tmp_score = score.split('#');
    //tmp_score[1] : O_Score.
    //tmp_score[2] : G_Score.
    //tmo_score[3] : Reason.
    
}

function congratulate(msg)
{
    console.log("CONGRATULATING:"+msg);

}
function get_ghost_color(color)
{
    console.log(color);  
}
function show_recommended_move(move) // in addition to valid moves, There can be a specific recommended move.
{

    console.log('Recommended Moves:'+ move);
    var tmp_move = move.split('#');
    //tmp_move[0] : move_type.
    // tmp_move[1] : move_position.
    var coord = tmp_move.split('-');
    //coord[0] : x , coord[1] :y . should be parsed as integers before used.
}

// white : '1' , black : '0'
function send_opponent_color(color){
    to_game.send(color);
}


function send_opponent_move(move_type,position){
    pos = position[0]+"-"+position[1];
    to_game.send(move_type+"#"+pos);
}
function send_mode(mode){
    to_game.send(mode);
    oppo_mode = mode; 
}


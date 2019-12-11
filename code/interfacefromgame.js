const gui = require("../js/main.js");
var zmq = require("zeromq");
var fs = require('fs');
var from_game = zmq.socket("pull");
from_game.connect("tcp://127.0.0.1:3001");
console.log("GUI from game interface started!");




//TO-DO : REPLACE PLACE HOLDERS. 
from_game.on("message", function(msg) {
    
        // console.log("work from pull: %s", msg.toString());
        result = msg.toString();
        l = result.split(',');
        
        switch(l[0]){
                case 'STATE':
                draw_state('../Game/send_state.txt');
                break;
            case 'VALID':
                draw_moves('../Game/valid_moves.txt');
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
                update_board('../Game/update_board.txt');
                break;
            case 'COLOR':
                get_ghost_color(l[1]);
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
                    state[i][j%3] = tmp[j];  
                    console.log(tmp[j]);
                }
            }
            //call gui function here. each row contains x,y,color.
            gui.drawState(state)
        } else {
            console.log(err);
        }
    })    
}



function draw_moves(file_name) // to draw valid moves.
{
    fs.readFile(file_name, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            // console.log('received data: ' + data);
            var tmp = data.split(',');
            var stone_count = (tmp.length-1)/2;
            var valid = new Array(stone_count);
            for(i = 0 ; i<stone_count;i++)
            {
                valid[i] = new Array(2);
                for(j = 2*i ; j<2*i+2; j++)
                {
                    valid[i][j%2] = tmp[j];  
                    // console.log(tmp[j]);
                }
            }
            gui.validMoves(valid);
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
    //var tmp_coord = tmp_move[1].split('-');
    //tmp_coord[0] : x , tmp_coord[1] = y.
    //gui_func()
    move = tmp_move[1].split('-');
    gui.drawMove(move, tmp_move[2], tmp_move[3], tmp_move[4]);
    
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
                    state[i][j%3] = tmp[j];  
                    console.log(tmp[j]);
                }
            }
            //call gui function here. each row contains x,y,color.
            gui.updateBoard(state)
        } else {
            console.log(err);
        }
    })    
}

function show_score(score)
{
    console.log('SCORE: '+score);
    var tmp_score = score.split('#');
    //tmp_score[0] : O_Score.
    //tmp_score[1] : G_ Score.
    //tmo_score[2] : Reason.
    gui.showScore(tmp_score[0], tmp_score[1], tmo_score[2]);
}

function congratulate(msg)
{
    console.log("CONGRATULATING:"+msg)
    gui.congratulate(msg);
}
function show_recommended_move(move) // in addition to valid moves, There can be a specific recommended move.
{

    console.log('Recommended Moves:'+ move);
    var tmp_move = move.split('#');
    //tmp_move[0] : move_type.
    // tmp_move[1] : move_position.
    var coord = tmp_move[1].split('-');
    //coord[0] : x , coord[1] :y . should be parsed as integers before used.
    gui.showRecommendedMove(tmp_move[0], coord);
}
function get_ghost_color(color)
{
    gui.get_ghost_color(color);
}

const interface = require("../interface.js");
const utilities = require("../js/utilities.js");
const color = sessionStorage.getItem('color');
const mode = sessionStorage.getItem('mode');
var my_turn = false;
var valid_moves = "all";
var ghost_animate = true;
const blockSz = 30;
const blockNum = 18;
const x = window.innerWidth/2 - (blockSz*blockNum)/2;
const y = 100;
var blurFilter = new PIXI.filters.BlurFilter();
blurFilter.blur = 0;
if(color == "black") my_turn = true;

console.log("index, color: ", color);

const app = new PIXI.Application({
	autoResize: true,
    resolution: devicePixelRatio,
});
document.body.appendChild(app.view);
var stage = new PIXI.Container();
app.stage.interactive = true;


var loader = new PIXI.Loader();
//Add all images
loader.add(['../images/mainbg.jpg','../images/Ghost Matter.jpg', '../images/ooh.png',
            "../images/sound.png", "../images/mute.png", '../images/pass.png',
            '../images/resign.png', '../images/timer.png', '../images/boardcartoon.png',
            "../images/white.png", "../images/black.png", "../images/red.png", '../images/score.png', ]);
loader.once('complete',setup);
loader.load();

function setup(){
    var bg = PIXI.Sprite.from('../images/mainbg.jpg');
    bg.height = window.innerHeight;
    bg.width = window.innerWidth;
    bg.filters = [blurFilter];
    app.stage.addChild(bg);
    // --------- animated ghost ----------------------------
    const cells = PIXI.Sprite.from('../images/Ghost Matter.jpg');
    cells.scale.set(5);

    const mask = PIXI.Sprite.from('../images/ooh.png');
    mask.anchor.set(0.5);
    mask.x = 310;
    mask.y = 190;

    cells.mask = mask;
    mask.filters = [blurFilter]; 
    cells.filters = [blurFilter]; 
    app.stage.addChild(mask, cells);
    const target = new PIXI.Point();
    reset();

    const textureAnimate = PIXI.Texture.from("../images/sound.png"); //modify//image
    const textureStop = PIXI.Texture.from("../images/mute.png");
    var ghostButton = PIXI.Sprite.fromImage(textureAnimate);
    ghostButton.x = 50
    ghostButton.y = 10
    ghostButton.height = 90
    ghostButton.width = 90 
    
    const ghostButtonRect = new PIXI.Graphics();
    ghostButtonRect.lineStyle(1, 0xffff);
    ghostButtonRect.drawCircle (ghostButton.x+ghostButton.width/2, ghostButton.y+ghostButton.height/2, 30)
    ghostButtonRect.hitArea = new PIXI.Circle(ghostButton.x+ghostButton.width/2, ghostButton.y+ghostButton.height/2, 30);
    ghostButtonRect.interactive = true;
    ghostButtonRect.buttonMode = true;

    ghostButtonRect.on('click', function(){
       if(ghost_animate) ghostButton.texture = textureStop;
       else ghostButton.texture = textureAnimate;
       ghost_animate = !ghost_animate;
    });
    app.stage.addChild(ghostButton);
    app.stage.addChild(ghostButtonRect);
    
    function reset() {
        target.x = Math.floor(Math.random() * app.renderer.width);
        target.y = Math.floor(Math.random() * app.renderer.height);
    }
    
    app.ticker.add(() => {
        if(ghost_animate){
            mask.x += (target.x - mask.x) * 0.1;
            mask.y += (target.y - mask.y) * 0.1;
    
            if (Math.abs(mask.x - target.x) < 1) {
                reset();
            }
        }
    });

    //--------------------------------BUTTONS----------------------------------
    const passButton = PIXI.Sprite.fromImage('../images/pass.png');
    passButton.x = 1200
    passButton.y = 550
    passButton.height = 90
    passButton.width = 200 

    const passButtonRect = new PIXI.Graphics();
    passButtonRect.lineStyle(1, 0xffff);
    passButtonRect.drawRect(1225,570, 150, 40);
    passButtonRect.hitArea = new PIXI.Rectangle(1225,570, 150, 40);
    passButtonRect.interactive = true;
    passButtonRect.buttonMode = true;

    if(mode == "AIVSHuman"){
        passButtonRect.on('click', function(){
            if(!my_turn) return;
            var red_stone = app.stage.getChildByName("red");
            if(red_stone != null)  app.stage.removeChild(red_stone);
            my_turn = false;
            interface.send_opponent_move("2");
        });
    }
    passButton.filters = [blurFilter];
    app.stage.addChild(passButton);
    app.stage.addChild(passButtonRect);
    
    const resignButton = PIXI.Sprite.fromImage('../images/resign.png');
    resignButton.x = 1200
    resignButton.y = 650
    resignButton.height = 90
    resignButton.width = 200 

    const resignButtonRect = new PIXI.Graphics();
    resignButtonRect.lineStyle(1, 0xffff);
    resignButtonRect.drawRect(1225,670, 150, 40);
    resignButtonRect.hitArea = new PIXI.Rectangle(1225,670, 150, 40);
    resignButtonRect.interactive = true;
    resignButtonRect.buttonMode = true;

    if(mode == "AIVSHuman"){
        resignButtonRect.on('click', function(){
            if(!my_turn) return;
            var red_stone = app.stage.getChildByName("red");
            if(red_stone != null)  app.stage.removeChild(red_stone);
            my_turn = false;
            interface.send_opponent_move("1");
        });
    }
    resignButton.filters = [blurFilter];
    app.stage.addChild(resignButton);
    app.stage.addChild(resignButtonRect);

    utilities.addSoundButton(app);
    addTimer();
    drawBoard();
    //showScore("2500","56100","TimeOut"); //modify //removetest
}

function addTimer(){
    if(mode != "AIVSHuman") return;

    const timerBoard = PIXI.Sprite.fromImage('../images/timer.png');
    timerBoard.x = 1010
    timerBoard.y = 130
    timerBoard.height = 200
    timerBoard.width = 500 
    timerBoard.filters = [blurFilter];
    app.stage.addChild(timerBoard); 

//--------------------------------TIMER-------------------------------------
    const timerStyle = new PIXI.TextStyle({
        fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
        dropShadow: true,
        dropShadowAlpha: 0.4,
        dropShadowColor: "silver",
        fill: '#3e1707', 
        fontSize : 50,
        align: 'center', 
        stroke: '#a4410e', strokeThickness: 7 
    });
    var seconds = 899;
    var remainTime = "15 : 00";
    var countingText = new PIXI.Text(remainTime,timerStyle);
    countingText . x = 1200;
    countingText.y = 175;
    countingText.filters = [blurFilter];
    app.stage.addChild(countingText);

    var tik = setInterval(countTimer , 1000);
    function countTimer()
    {
        if(!my_turn) return;
        console.log("timer")
        var min = Math.floor(seconds / 60);
        var remainSeconds = seconds % 60;
        if(min == 0 && remainSeconds == 0) remainTime = "TIME OUT";
        else{
            if(seconds < 10) remainSeconds = "0" + remainSeconds;
            if(min < 10) min = "0" + min;
            remainTime = min + " : " + remainSeconds;
            seconds -= 1;
        }
        countingText.text = remainTime;
    }
}


 

function drawBoard(){
    const board = PIXI.Sprite.fromImage('../images/boardcartoon.png');
    board.interactive = true;
    margin =  30;
    board.x = x - margin;
    board.y = y - margin;
    board.height = blockSz*blockNum + 2*margin;
    board.width = blockSz*blockNum + 2*margin;

    if(mode == "AIVSHuman") board.on('pointerup', onClick);
    board.filters = [blurFilter];
    app.stage.addChild(board);

    drawLetters();
    drawNumbers();
    drawGrid();
}

function inGrid(clickX, clickY){
    const flexibility = 10;
    var clickXX = Math.floor(clickX);
    var clickYY = Math.floor(clickY);
    console.log("x: ", clickX, "y ", clickY);
    clickXX -= x;
    clickYY -= y;
    if(clickXX + flexibility < 0 || clickYY + flexibility < 0) return false;
    if(clickXX - flexibility > blockNum*blockSz || clickYY - flexibility > blockNum*blockSz) return false;    
    return true;
}


function onClick(event){
    console.log("board on click");
    if(!my_turn) return;
    var clickPosX = event.data.global.x ;
    var clickPosY = event.data.global.y ;
    if(inGrid(clickPosX, clickPosY)){
        const texture_white_stone = PIXI.Texture.from("../images/white.png");
        const texture_back_stone = PIXI.Texture.from("../images/black.png");
        const texture_red_stone = PIXI.Texture.from("../images/red.png");
        var stone = PIXI.Sprite.fromImage(texture_white_stone);
        
        clickPosX = Math.round(clickPosX / blockSz) * blockSz;
        clickPosY = Math.floor(clickPosY / blockSz) * blockSz;

        stone.x = clickPosX - blockSz/2;
        stone.y = clickPosY;
        stone.height = 25;
        stone.width = 25;

        col = clickPosX - x;
        row = clickPosY - y;
        col = col / blockSz;
        row = row / blockSz;
        col = Math.ceil(col);
        row = Math.ceil(row);

        var rowNum = 19-row;
        var colChar = String.fromCharCode(65+col);
        if(colChar >= 'I') colChar = String.fromCharCode(65+col+1);
        var move = "#" + colChar + '-' + rowNum;
        //check it //modify//indexOf != -1
        //if valid move
        if(valid_moves == "all" || valid_moves.includes(move)){
            //modify //Assume return null if not found
            var red_stone = app.stage.getChildByName("red");
            if(red_stone != null)  app.stage.removeChild(red_stone);
            if(color === "black" ) stone.texture = texture_back_stone;
            move = "0"+move;
            my_turn = false;
            interface.send_opponent_move(move); 
            stone.filters = [blurFilter];
            app.stage.addChild(stone);
        }
        
        else{
            stone.texture = texture_red_stone;
            stone.name("red");
            stone.filters = [blurFilter];
            app.stage.addChild(stone);
            app.removeChild()
        }
    }
 
}


function drawLetters(){
    var i;
    var letterUp;
    var letterDown;
    var posX = x-5;
    var posY = y;

    for(i = 0; i<20; i++){
        if(String.fromCharCode(65+i) == "I") continue;
        const fontStyle = new PIXI.TextStyle({
            dropShadow: true,
            dropShadowAlpha: 0.4,
            dropShadowColor: "silver",
            //fontColor : 0x452000,
            fill: '#3e1707', 
            fontSize: 20 ,
            fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
            fontStyle: "italic",
            fontWeight: "bold",stroke: '#a4410e', strokeThickness: 3
        });
        letterUp = new PIXI.Text(String.fromCharCode(65+i),fontStyle);
        letterUp.fo
        letterDown = new PIXI.Text(String.fromCharCode(65+i),fontStyle);
        letterUp.x = posX;
        letterDown.x = posX;
        letterUp.y = y - margin;
        letterDown.y = blockSz*blockNum + y + 5; 
        letterDown.filters = [blurFilter]; 
        letterUp.filters = [blurFilter]; 
        app.stage.addChild(letterUp);
        app.stage.addChild(letterDown);
        posX += blockSz;
    }
}

function drawNumbers(){
    var i;
    var numLeft;
    var numRight;
    var posX = x;
    var posY = y - 10;

    const numStyle = new PIXI.TextStyle({
        dropShadow: true,
        dropShadowAlpha: 0.4,
        dropShadowColor: "silver",
        fill: '#3e1707', 
        fontSize: 20 ,
        fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
        fontStyle: "italic",
        fontWeight: "bold",stroke: '#a4410e', strokeThickness: 3 
    });

    for(i = 19; i>0; i--){
        numLeft = new PIXI.Text(String(i),numStyle);
        numRight = new PIXI.Text(String(i),numStyle);
        numLeft.x = posX - margin;
        numRight.x = blockSz*blockNum + x + 5;
        if(i < 10){
            numLeft.x += 5;
            numRight.x += 5;
        }
        numLeft.y = posY;
        numRight.y = posY;
        numLeft.filters = [blurFilter]; 
        numRight.filters = [blurFilter]; 
        app.stage.addChild(numLeft);
        app.stage.addChild(numRight);
        posY += blockSz;
    }
}


function drawGrid(){
    var grid = new PIXI.Graphics();
    grid.lineStyle(3, 0x000000, 1);
    grid.drawRect(x , y, blockSz*blockNum, blockSz*blockNum);

    var i;
    var posX = x;
    var posY = y;

    //vertical lines
    for (i = 0; i < blockNum; i++){
        posX += blockSz;
        grid.moveTo(posX, y);
        grid.lineTo(posX, blockSz*blockNum + y);
    }

    posX = x;
    //horizontal lines
    for (i = 0; i < blockNum; i++){
        posY += blockSz;
        grid.moveTo(x, posY);
        grid.lineTo(blockSz*blockNum + x, posY);
    }

    grid.filters = [blurFilter]; 
    app.stage.addChild(grid);
}


function validMoves(moves){
    valid_moves = moves;
}

function drawMove(move, AIColor){
    if(mode == "AIVSHuman") my_turn = true;
    
    move = move.toString();
    if(move[0] != '0') return;
    if(mode == "AIVSHuman"){
        if(color === "white" ) var stone = PIXI.Sprite.fromImage('../images/black.png');
        else var stone = PIXI.Sprite.fromImage('../images/white.png');
    }
    else color = AIColor;
        
    l = move.split('#');
    l = l[1].split('-');
    var colChar = l[0];
    var rowNum = l[1];

    var row = 19 - parseInt(rowNum, 10);;
    col = colChar.charCodeAt(0)-65;
    if(colChar >= 'I') --col;
   
    col = col*blockSz + x;
    row = row*blockSz + y;
    console.log("added stone col: ", col , " row ", row);

    col = Math.round(col / blockSz) * blockSz;
    row = Math.floor(row / blockSz) * blockSz;

    stone.x = col - blockSz/2;
    stone.y = row;
    stone.height = 25;
    stone.width = 25;
    stone.filters = [blurFilter]; 
    app.stage.addChild(stone);
}


function showScore(O_score,G_score,reason){
    my_turn = false;
    ghost_animate = false;
    blurFilter.blur = 5;


    const fontStyle1 = new PIXI.TextStyle({
        dropShadow: true,
        dropShadowAlpha: 0.4,
        dropShadowColor: "silver",
        //fontColor : 0x452000,
        fill: '#3e1707', 
        fontSize: 90 ,
        fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
        fontStyle: "italic",
        fontWeight: "bold",stroke: '#a4410e', strokeThickness: 9
    });

    const fontStyle2 = new PIXI.TextStyle({
        dropShadow: true,
        dropShadowAlpha: 0.4,
        dropShadowColor: "silver",
        //fontColor : 0x452000,
        fill: '#3e1707', 
        fontSize: 50 ,
        fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
        fontStyle: "italic",
        fontWeight: "bold",stroke: '#a4410e', strokeThickness: 9
    });

    const myScoreBoard = PIXI.Sprite.fromImage('../images/score.png');
    myScoreBoard.x = 110
    myScoreBoard.y = 300
    myScoreBoard.height = 90
    myScoreBoard.width = 200 
    app.stage.addChild(myScoreBoard);

    var myScoreTxt = new PIXI.Text(G_score,fontStyle2);
    myScoreTxt.x = myScoreBoard.x + myScoreBoard.width /2 - myScoreTxt.width/2;
    myScoreTxt.y = 300
    app.stage.addChild(myScoreTxt);

    GScoreStr = new PIXI.Text("Ghost Score",fontStyle2);
    GScoreStr.x = myScoreBoard.x + myScoreBoard.width/2 - GScoreStr.width/2;
    GScoreStr.y = 200
    app.stage.addChild(GScoreStr);


    const opponentScoreBoard = PIXI.Sprite.fromImage('../images/score.png');
    opponentScoreBoard.x = 110
    opponentScoreBoard.y = 500
    opponentScoreBoard.height = 90
    opponentScoreBoard.width = 200 
    app.stage.addChild(opponentScoreBoard);

    var opponentScoreTxt = new PIXI.Text(O_score,fontStyle2);
    opponentScoreTxt.x = opponentScoreBoard.x + opponentScoreBoard.width /2 - opponentScoreTxt.width/2;
    opponentScoreTxt.y = 500
    app.stage.addChild(opponentScoreTxt);

    if(mode == "AIVSHuman") OScore = "Your Score"
    else OScore = "Opponent Score"
    OScoreStr = new PIXI.Text(OScore, fontStyle2);
    OScoreStr.x = opponentScoreBoard.x + opponentScoreBoard.width/2 - OScoreStr.width/2;
    OScoreStr.y = 400
    app.stage.addChild(OScoreStr);

    msg = "Hard Luck"
    if(G_score < O_score){
        // //modify //add image//z3lan
        if(mode == "AIVSHuman") msg = "Congratulations"
    } 
    else if (G_score > O_score){
        // //modify //add image//fr7an
        if(mode != "AIVSHuman") msg = "Congratulations"
    }
    else if(G_score == O_score){
        // //modify //add image
        msg = "Tie"
    } 

    GScoreStr = new PIXI.Text(msg,fontStyle1);
    GScoreStr.x = window.innerWidth/2 - GScoreStr.width/2;
    GScoreStr.y = y
    app.stage.addChild(GScoreStr);

    reasonStr = new PIXI.Text(reason,fontStyle2);
    reasonStr.x = window.innerWidth/2 - reasonStr.width/2;
    reasonStr.y = y + blockSz*blockNum + 30
    app.stage.addChild(reasonStr);
}

function congratulate(msg){
    
}

function showRecommendedMove(move){

}

// Listen for window resize events
window.addEventListener('resize', resize);
// Resize function window
function resize() {
	// Resize the renderer
	app.renderer.resize(window.innerWidth, window.innerHeight);
}
resize();

module.exports = {drawMove, validMoves, showScore, congratulate, showRecommendedMove};


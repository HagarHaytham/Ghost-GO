const remote = require('electron').remote;
const interface = require("../interface.js");
const utilities = require("../js/utilities.js");
var color = sessionStorage.getItem('color');
const mode = sessionStorage.getItem('mode');
if(mode =="AIVSAI") interface.send_mode('1');
else interface.send_mode('0');

if(color == "black") interface.send_opponent_color('0');
else interface.send_opponent_color('1');

var LastMove_pass = true
var scoreScreen = false
var my_turn = false;
var valid_moves = [[-1,-1]];
var ghost_animate = true;
const blockSz = 30;
const blockNum = 18;
var initialState = false;
if(mode == "AIVSHuman") initialState = true; //test
var initialStateColor = "Black"
var initialBorad = [];
const x = 450;
const y = 100;
var blurFilter = new PIXI.filters.BlurFilter();
blurFilter.blur = 0;

var blurFilter2= new PIXI.filters.BlurFilter();
blurFilter2.blur = 0;
if(color == "black") my_turn = true;

//console.log("index, color: ", color);

const app = new PIXI.Application({
	autoResize: true,
    resolution: devicePixelRatio,
});
document.body.appendChild(app.view);
var stage = new PIXI.Container();
app.stage.interactive = true;

//------------yourTurn-----------------
fontStyle2 = utilities.getFontStyle(50);
yourTurnStr = new PIXI.Text("your turn!",fontStyle2);
yourTurnStr.x = window.innerWidth/2 - yourTurnStr.width/2;
yourTurnStr.y = y + blockSz*blockNum + 30
yourTurnStr.name = "yourturn";
yourTurnStr.filters = [blurFilter]; 
if(!my_turn || initialState) yourTurnStr.visible = false;
else yourTurnStr.visible = true;
///-----------------------------
var passButton
var passButtonRect
var resignButtonRect
var resignButton
var playButton
var playButtonRect
//--------------Timer-------------------
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

var remainTime = "15 : 00" //test
var GCountingTxt = new PIXI.Text(remainTime,timerStyle);
GCountingTxt.x = 1200;
GCountingTxt.y = 175;
GCountingTxt.filters = [blurFilter];

var OCountingTxt = new PIXI.Text(remainTime,timerStyle);
OCountingTxt.x = 1200;
OCountingTxt.y = 385;
OCountingTxt.filters = [blurFilter];
//////////////////////////////////////////////

var loader = new PIXI.Loader();
//Add all images
loader.add(['../images/mainbg.jpg','../images/Ghost Matter.jpg', '../images/ooh.png',
            "../images/sound.png", "../images/mute.png", '../images/pass.png',
            '../images/resign.png', '../images/timer.png', '../images/boardcartoon.png',
            "../images/white.png", "../images/black.png", "../images/red.png", '../images/score.png', '../images/dab.png', '../images/done.png']);
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
    //app.stage.addChild(ghostButtonRect);
    //app.stage.addChild(ghostButton);
    
    
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
    passButton = PIXI.Sprite.fromImage('../images/pass.png');
    passButton.x = 1200
    passButton.y = 550
    passButton.height = 90
    passButton.width = 200 

    passButtonRect = new PIXI.Graphics();
    passButtonRect.lineStyle(1, 0xffff);
    passButtonRect.drawRect(1225,570, 150, 40);
    passButtonRect.hitArea = new PIXI.Rectangle(1225,570, 150, 40);
    passButtonRect.interactive = true;
    passButtonRect.buttonMode = true;
    if(mode == "AIVSHuman"){
        passButtonRect.on('click', function(){
            if(!my_turn) return;
            utilities.removeChildByName("red", app);
            var congratulateStr = app.stage.getChildByName("congratulate");
            if(congratulateStr != null)  app.stage.removeChild(congratulateStr);

            my_turn = false;
            yourTurnStr.visible = false;
            LastMove_pass = true;
            interface.send_opponent_move("2", []);
        });
    }
    passButton.filters = [blurFilter];
    app.stage.addChild(passButtonRect);
    app.stage.addChild(passButton);
    
    
    resignButton = PIXI.Sprite.fromImage('../images/resign.png');
    resignButton.x = 1200
    resignButton.y = 650
    resignButton.height = 90
    resignButton.width = 200 

    resignButtonRect = new PIXI.Graphics();
    resignButtonRect.lineStyle(1, 0xffff);
    resignButtonRect.drawRect(1225,670, 150, 40);
    resignButtonRect.hitArea = new PIXI.Rectangle(1225,670, 150, 40);
    resignButtonRect.interactive = true;
    resignButtonRect.buttonMode = true;

    if(initialState){
        passButton.visible = false
        passButtonRect.visible = false
        resignButtonRect.visible = false
        resignButton.visible = false
    }

    if(mode == "AIVSHuman"){
        resignButtonRect.on('click', function(){
            if(!my_turn) return;

            utilities.removeChildByName("red", app);

            var congratulateStr = app.stage.getChildByName("congratulate");
            if(congratulateStr != null)  app.stage.removeChild(congratulateStr);

            LastMove_pass = true;
            my_turn = false;
            yourTurnStr.visible = false;
            interface.send_opponent_move("1", []);
        });
    }
    else{
        passButtonRect.visible = false;
        passButton.visible = false;
        resignButtonRect.visible = false;
        resignButton.visible = false;
    }
    resignButton.filters = [blurFilter];
    app.stage.addChild(resignButtonRect);
    app.stage.addChild(resignButton);
    app.stage.addChild(yourTurnStr);

    utilities.addSoundButton(app);
    if(initialState == true && mode == "AIVSHuman") addInitialState(); //test
    addTimer();
    drawBoard();
    //addPlayAgainButton();
    //addExitButton();
    //-----------------------TESTING--------------------------
    //drawMove(['5','19'], '0', "14:00", "13:00")
    //boardtmp = [['1','19','0'], ['2','19','1'], ['3','18','1'], ['4','17','0']]
    //updateBoard(boardtmp);
    //drawState(boardtmp);
    //congratulate("Nice Move")
    
    //drawMove(['5','13'], '0', "14:00", "13:00")
    //drawMove(['6','18'], '1', "13:00", "12:00")
    //showRecommendedMove('0',['1','18']); //place
    //showScore("2500","56100","you Resigned");
    //updateBoard(boardtmp)
    //showRecommendedMove('1',['1','19']); //resign
    //showRecommendedMove('2',['1','19']); //pass
    //getGhostColor("1");
    //validMoves([['1','19']])
    //updateGhostTime("815548");
    //updateopponentTime("95556")
}

function addInitialState(){
    fontStyle2 = utilities.getFontStyle(30);
    msg3Txt = new PIXI.Text("Draw Initial State", fontStyle2);
    msg3Txt.x = x + (blockNum*blockSz)/2 - msg3Txt.width/2;
    msg3Txt.y = y - 80
    msg3Txt.name = "initial"
    app.stage.addChild(msg3Txt);

    msg1Txt = new PIXI.Text(initialStateColor, fontStyle2);
    msg1Txt.x = x/2 - msg1Txt.width/2;
    msg1Txt.y = 200
    msg1Txt.name = "initial";
    app.stage.addChild(msg1Txt);

    const doneButton = PIXI.Sprite.fromImage('../images/done.png');
    doneButton.x = msg1Txt.x - 50
    doneButton.y = 300
    doneButton.height = 90
    doneButton.width = 200 
    doneButton.name = "initial"

    const doneButtonRect = new PIXI.Graphics();
    doneButtonRect.lineStyle(1, 0xffff);
    doneButtonRect.drawRect(doneButton.x+25,320, 150, 40);
    doneButtonRect.hitArea = new PIXI.Rectangle(doneButton.x+25,320, 150, 40);
    doneButtonRect.interactive = true;
    doneButtonRect.buttonMode = true;
    doneButtonRect.name = "initial"
    
    app.stage.addChild(doneButtonRect)
    app.stage.addChild(doneButton)
    

    doneButtonRect.on('click', function(){
        if(initialStateColor  == "Black"){
            initialStateColor = "White"
            msg1Txt.text = initialStateColor ;
        }
        else{
            sendInitialBoard(initialBorad)
            initialState = false;
            //console.log("after initial state")
            utilities.removeChildByName("initial", app)
            passButton.visible = true
            passButtonRect.visible = true
            resignButtonRect.visible = true
            resignButton.visible = true
            if(my_turn) yourTurnStr.visible = true
        } 
    });
}

function addTimer(){
    const timerBoard = PIXI.Sprite.fromImage('../images/timer.png');
    timerBoard.x = 1010
    timerBoard.y = 130
    timerBoard.height = 200
    timerBoard.width = 500 
    timerBoard.filters = [blurFilter];
    app.stage.addChild(timerBoard); 

    if(mode != "AIVSHuman"){
        const fontStyle = utilities.getFontStyle(50);
        const timerBoardTxt = new PIXI.Text("Ghost",fontStyle);
        timerBoardTxt.x = timerBoard.x + timerBoard.width/2 - timerBoardTxt.width/2 + 20
        timerBoardTxt.y = 70
        timerBoardTxt.filters = [blurFilter];
        app.stage.addChild(timerBoardTxt); 

        const timerBoardTxt2 = new PIXI.Text("opponent",fontStyle);
        timerBoardTxt2.x = timerBoard.x + timerBoard.width/2 - timerBoardTxt2.width/2 + 20
        timerBoardTxt2.y = 280
        timerBoardTxt2.filters = [blurFilter];
        app.stage.addChild(timerBoardTxt2); 

        const timerBoard2 = PIXI.Sprite.fromImage('../images/timer.png');
        timerBoard2.x = 1010
        timerBoard2.y = 340
        timerBoard2.height = 200
        timerBoard2.width = 500 
        timerBoard2.filters = [blurFilter];
        app.stage.addChild(timerBoard2); 

        app.stage.addChild(GCountingTxt);
        app.stage.addChild(OCountingTxt);
        return;
    }

//--------------------------------TIMER-------------------------------------
    var seconds = 899;
    var remainTimeTmp = "15 : 00"; //test
    var countingText = new PIXI.Text(remainTimeTmp,timerStyle);
    countingText . x = 1200;
    countingText.y = 175;
    countingText.filters = [blurFilter];
    app.stage.addChild(countingText);

    var tik = setInterval(countTimer , 1000);
    function countTimer()
    {
        if(!my_turn || initialState) return;
        var min = Math.floor(seconds / 60);
        var remainSeconds = seconds % 60;
        if(min == 0 && remainSeconds == 0){
            utilities.removeChildByName("red", app);
            
            var congratulateStr = app.stage.getChildByName("congratulate");
            if(congratulateStr != null)  app.stage.removeChild(congratulateStr);
            
            my_turn = false;
            yourTurnStr.visible = false;
            interface.send_opponent_move("1", []);
            remainTimeTmp = "TIME OUT";
            countingText . x = 1150;
        } 
        else{
            var remainSecondsStr = remainSeconds.toString()
            var minStr = min.toString()
            if(remainSeconds < 10) remainSecondsStr = "0" + remainSecondsStr;
            console.log("remainSeconds",remainSecondsStr)
            if(min < 10) minStr = "0" + minStr;
            remainTimeTmp = minStr + " : " + remainSecondsStr;
            seconds -= 1;
        }
        countingText.text = remainTimeTmp;
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
    //console.log("x: ", clickX, "y ", clickY);
    clickXX -= x;
    clickYY -= y;
    if(clickXX + flexibility < 0 || clickYY + flexibility < 0) return false;
    if(clickXX - flexibility > blockNum*blockSz || clickYY - flexibility > blockNum*blockSz) return false;    
    return true;
}


function onClick(event){
    //console.log("board on click");
    if(!my_turn && !initialState) return;
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

        ++col;
        ++row;
        var move = [col.toString(), row.toString()];
        //check it //modify//indexOf != -1
        //console.log("move ", move [0], " y ", move[1])
        
        if(initialState){
            if(initialStateColor == "White" ){
                stone.texture = texture_white_stone;
                move.push('1');
            } 
            else{
                stone.texture = texture_back_stone;
                move.push('0')
            } 
            
            if(!utilities.isItemInArray(initialBorad, move)){
                //console.log("isn't in item")
                initialBorad.push(move)
                stone.name = "stone"
                stone.filters = [blurFilter];
                app.stage.addChild(stone);
            }
            return;

        }
        //console.log(utilities.isItemInArray(valid_moves, [-1,-1]));
        //console.log(utilities.isItemInArray(valid_moves, move));
        if(utilities.isItemInArray(valid_moves, [-1,-1]) || utilities.isItemInArray(valid_moves, move)){
            //modify //Assume return null if not found
            utilities.removeChildByName("red", app)

            var congratulateStr = app.stage.getChildByName("congratulate");
            if(congratulateStr != null)  app.stage.removeChild(congratulateStr);

            if(color === "black" ) stone.texture = texture_back_stone;
            my_turn = false;
            yourTurnStr.visible = false;
            interface.send_opponent_move("0", move); 
            //console.log("move x ",  move[0] , " y ", move[1]);
            stone.filters = [blurFilter];
            stone.name = "stone"
            app.stage.addChild(stone);

            LastMove_pass = false;
        }
        
        else{
            stone.texture = texture_red_stone;
            stone.name = "red";
            stone.filters = [blurFilter];
            app.stage.addChild(stone);
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

function drawMove(move, tmpColorNum, GTime, OTime){
    var tmpColor;
    //console.log("move x ", move[0], " y ", move[1])
    
    if(mode == "AIVSHuman"){
        if(GTime != "color"){
            my_turn = true;
            yourTurnStr.visible = true;
            if(color == "black") tmpColor = 'white'
            else tmpColor = 'black'
        }
        else{
            if(tmpColorNum == '0') tmpColor = 'black'
            else tmpColor = 'white'
        }
    } 
    else{
        if(GTime != 'color'){
            updateGhostTime(GTime);
            updateopponentTime(OTime);
        }
        if(tmpColorNum == '0') tmpColor = 'black'
        else tmpColor = 'white'
    }

    utilities.removeChildByName("red", app)

    var congratulateStr = app.stage.getChildByName("congratulate");
    if(congratulateStr != null)  app.stage.removeChild(congratulateStr);

    if(move.length == 0) return; //modify //display if passed
    if(tmpColor == "white" ) var stone = PIXI.Sprite.fromImage('../images/white.png');
    else var stone = PIXI.Sprite.fromImage('../images/black.png');
   
    var row = parseInt(move[1], 10);
    var col = parseInt(move[0], 10);
    --row;
    --col;
    col = col*blockSz + x;
    row = row*blockSz + y;
    //console.log("added stone col: ", col , " row ", row);

    col = Math.round(col / blockSz) * blockSz;
    row = Math.floor(row / blockSz) * blockSz;

    stone.x = col - blockSz/2;
    stone.y = row;
    stone.height = 25;
    stone.width = 25;
    stone.filters = [blurFilter]; 
    stone.name = "stone"
    app.stage.addChild(stone);
}


function showScore(O_score,G_score,reason){
    my_turn = false;
    yourTurnStr.visible = false;
    ghost_animate = false;
    blurFilter.blur = 5;
    scoreScreen = true;
    blurFilter2.blur = 5
    //undo for exit, playAgain btns
    /*if(mode == "AIVSHuman"){
        playButton.visible = true
        playButtonRect.visible = true
            
        exitButton.visible = true
        exitButtonRect.visible = true
    } */
    
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
    myScoreBoard.name = "scorescreen"
    app.stage.addChild(myScoreBoard);

    var myScoreTxt = new PIXI.Text(G_score,fontStyle2);
    myScoreTxt.x = myScoreBoard.x + myScoreBoard.width /2 - myScoreTxt.width/2;
    myScoreTxt.y = 300
    myScoreTxt.name = "scorescreen"
    app.stage.addChild(myScoreTxt);

    GScoreStr = new PIXI.Text("Ghost Score",fontStyle2);
    GScoreStr.x = myScoreBoard.x + myScoreBoard.width/2 - GScoreStr.width/2;
    GScoreStr.y = 200
    GScoreStr.name = "scorescreen"
    app.stage.addChild(GScoreStr);


    const opponentScoreBoard = PIXI.Sprite.fromImage('../images/score.png');
    opponentScoreBoard.x = 110
    opponentScoreBoard.y = 500
    opponentScoreBoard.height = 90
    opponentScoreBoard.width = 200 
    opponentScoreBoard.name = "scorescreen"
    app.stage.addChild(opponentScoreBoard);

    var opponentScoreTxt = new PIXI.Text(O_score,fontStyle2);
    opponentScoreTxt.x = opponentScoreBoard.x + opponentScoreBoard.width /2 - opponentScoreTxt.width/2;
    opponentScoreTxt.y = 500
    opponentScoreTxt.name = "scorescreen"
    app.stage.addChild(opponentScoreTxt);

    if(mode == "AIVSHuman") OScore = "Your Score"
    else OScore = "Opponent Score"
    OScoreStr = new PIXI.Text(OScore, fontStyle2);
    OScoreStr.x = opponentScoreBoard.x + opponentScoreBoard.width/2 - OScoreStr.width/2;
    OScoreStr.y = 400
    OScoreStr.name = "scorescreen"
    app.stage.addChild(OScoreStr);

    msg = "Hard Luck"
    G_score_int = parseFloat(G_score);
    O_score_int = parseFloat(O_score);
    if(G_score_int < O_score_int){
        // //modify //add image//z3lan
        if(mode == "AIVSHuman") msg = "Congratulations"
    } 
    else if (G_score_int > O_score_int){
        
        const logo = PIXI.Sprite.fromImage('../images/dab.png');
        logo.x =  window.innerWidth/2 - GScoreStr.width/2;;
        logo.y = y + 150;
        logo.scale.set(0.5);
        logo.name = "scorescreen"
        app.stage.addChild(logo);

        if(mode != "AIVSHuman") msg = "Congratulations"
    }
    else if(G_score_int == O_score_int){
        // //modify //add image
        msg = "Tie"
    } 

    GScoreStr = new PIXI.Text(msg,fontStyle1);
    GScoreStr.x = window.innerWidth/2 - GScoreStr.width/2 - 50;
    GScoreStr.y = y
    GScoreStr.name = "scorescreen"
    app.stage.addChild(GScoreStr);

    reasonStr = new PIXI.Text(reason,fontStyle2);
    reasonStr.x = window.innerWidth/2 - reasonStr.width/2;
    reasonStr.y = y + blockSz*blockNum + 30
    reasonStr.name = "scorescreen"
    if(mode != "AIVSHuman") app.stage.addChild(reasonStr);
}


function congratulate(msg){
    //console.log("cong")
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

    msgTxt = new PIXI.Text(msg,fontStyle2);
    msgTxt.x = x/2 - msgTxt.width/2;
    msgTxt.y = 200
    msgTxt.name = "congratulate";
    msgTxt.filters = [blurFilter];
    app.stage.addChild(msgTxt);
}


//Assume lsa mb3tsh l AI move //modify 
//Asssume not my turn so no clicks
function showRecommendedMove(moveType, move){
    var alerted = 0;
    blurFilter.blur = 5;
    var lastMove
    if(!LastMove_pass) {
         lastMove= app.stage.getChildAt(app.stage.children.length-1);
         app.stage.removeChildAt(app.stage.children.length-1); 
    }
    
    fontStyle2 = utilities.getFontStyle(30);
    msg1Txt = new PIXI.Text("Recommended Move",fontStyle2);
    msg1Txt.x = x/2 - msg1Txt.width/2;
    msg1Txt.y = 200
    msg1Txt.name = "alert1";
    msg1Txt.filters = [blurFilter2];
    app.stage.addChild(msg1Txt);

    msg2Txt = new PIXI.Text("Click here to Continue",fontStyle2);
    msg2Txt.x = x/2 - msg2Txt.width/2;
    msg2Txt.y = 300
    msg2Txt.name = "alert2";
    msg2Txt.interactive = true;
    msg2Txt.buttonMode = true;
    msg2Txt.filters = [blurFilter2];
    app.stage.addChild(msg2Txt);

    msg2Txt.on("click",function(){
        alerted = 1;
        blurFilter.blur = 0;
        utilities.removeChildByName("alert1",app);
        utilities.removeChildByName("alert2",app);
        utilities.removeChildByName("green",app);
        if(!LastMove_pass) app.stage.addChild(lastMove);
    });

    if (moveType == '0'){
        const stone = PIXI.Sprite.fromImage('../images/green.png');

        var row = parseInt(move[1], 10);
        var col = parseInt(move[0], 10);
        //console.log("added stone col: ", col , " row ", row);
        --row;
        --col;

        col = col*blockSz + x;
        row = row*blockSz + y;
        //console.log("added stone col: ", col , " row ", row);

        col = Math.round(col / blockSz) * blockSz;
        row = Math.floor(row / blockSz) * blockSz;

        stone.x = col - blockSz/2;
        stone.y = row;
        stone.height = 25;
        stone.width = 25;
        stone.name = "green"
        stone.filters = [blurFilter2];
        app.stage.addChild(stone);
    }
    else{
        if(moveType == '1') msg = "Resign"
        else msg = "Pass"
        fontStyle2 = utilities.getFontStyle(30);
        msg3Txt = new PIXI.Text(msg,fontStyle2);
        msg3Txt.x = x + (blockNum*blockSz)/2 - msg3Txt.width/2;
        msg3Txt.y = 200
        msg3Txt.name = "green"
        msg3Txt.filters = [blurFilter2];
        app.stage.addChild(msg3Txt);    
    }
}

function drawState(state){
    for(i = 0; i<state.length; ++i){
        drawMove([state[i][0],state[i][1]], state[i][2], "color", "color")
    }
      
}

function updateBoard(state){
    if(scoreScreen){
        ghost_animate = true;
        blurFilter.blur = 0;
        blurFilter2.blur = 0;
        utilities.removeChildByName("scorescreen", app)
        updateGhostTime("15 : 00");
        updateopponentTime("15 : 00");  
        alerted = 1;
        utilities.removeChildByName("alert1",app);
        utilities.removeChildByName("alert2",app);
        utilities.removeChildByName("green",app); 
        scoreScreen = false;     
    }

    //console.log("update board func")
    //remove all stones
    utilities.removeChildByName("stone", app);
    drawState(state)
}

function updateGhostTime(remainingtime){
    time = parseInt(remainingtime, 10);
    sec = Math.floor(time/1000);
    min = Math.floor(sec/60);
    sec = Math.floor(sec%60);
    var minStr = min.toString()
    var secStr = sec.toString()
    if(min < 10) minStr = "0" + minStr
    if(sec < 10) secStr = "0" + secStr
    remainingtime = minStr + " : " + secStr
    GCountingTxt.text = remainingtime;
}

function updateopponentTime(remainingtime){
    time = parseInt(remainingtime, 10);
    sec = Math.floor(time/1000);
    min = Math.floor(sec/60);
    sec = Math.floor(sec%60);
    var minStr = min.toString()
    var secStr = sec.toString()
    if(min < 10) minStr = "0" + minStr
    if(sec < 10) secStr = "0" + secStr
    remainingtime = minStr + " : " + secStr
    OCountingTxt.text = remainingtime;
}

function getGhostColor(AIColor){
    if(AIColor == '0')  color = "Black"
    else color = "White"
    fontStyle2 = utilities.getFontStyle(30);
    var msg = "Ghost Color is " + color
    msg3Txt = new PIXI.Text(msg, fontStyle2);
    msg3Txt.x = x + (blockNum*blockSz)/2 - msg3Txt.width/2;
    msg3Txt.y = y - 80
    app.stage.addChild(msg3Txt);    
}

function sendInitialBoard(board){
    interface.send_initial_board(board)
}

function addPlayAgainButton(){
    playButton = PIXI.Sprite.fromImage('../images/resign.png');
    playButton.x = 1200
    playButton.y = 550
    playButton.height = 90
    playButton.width = 200 

    playButtonRect = new PIXI.Graphics();
    playButtonRect.lineStyle(1, 0xffff);
    playButtonRect.drawRect(1225,570, 150, 40);
    playButtonRect.hitArea = new PIXI.Rectangle(1225,570, 150, 40);
    playButtonRect.interactive = true;
    playButtonRect.buttonMode = true;
    if(mode == "AIVSHuman"){
        playButtonRect.on('click', function(){
            location.assign("../html/mode.html"); 
            //close socket#modify
        });
    }
    playButton.visible = false
    playButtonRect.visible = false
    app.stage.addChild(playButtonRect);
    app.stage.addChild(playButton);

}
 
function addExitButton(){
    exitButton = PIXI.Sprite.fromImage('../images/pass.png');
    exitButton.x = 1200
    exitButton.y = 650
    exitButton.height = 90
    exitButton.width = 200 

    exitButtonRect = new PIXI.Graphics();
    exitButtonRect.lineStyle(1, 0xffff);
    exitButtonRect.drawRect(1225,670, 150, 40);
    exitButtonRect.hitArea = new PIXI.Rectangle(1225,670, 150, 40);
    exitButtonRect.interactive = true;
    exitButtonRect.buttonMode = true;

    exitButtonRect.on('click', function(){
        var window = remote.getCurrentWindow();
        window.close(); 
        //close socket#modify
    });
    
    exitButton.visible = false
    exitButtonRect.visible = false
    app.stage.addChild(exitButtonRect);
    app.stage.addChild(exitButton);

}

// Listen for window resize events
window.addEventListener('resize', resize);
// Resize function window
function resize() {
	// Resize the renderer
	app.renderer.resize(window.innerWidth, window.innerHeight);
}
resize();

module.exports = {drawMove, validMoves, showScore, congratulate, showRecommendedMove,
                  drawState, updateBoard, getGhostColor};



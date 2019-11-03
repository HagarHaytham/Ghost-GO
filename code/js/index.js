

const app = new PIXI.Application({
	autoResize: true,
  resolution: devicePixelRatio,
  //width: 1080,
  //height: 720
});

document.body.appendChild(app.view);
//app.renderer.backgroundColor = 0xB5672E;

var stage = new PIXI.Container();
app.stage.interactive = true;

//
var bg = PIXI.Sprite.from('../images/6.jpg');
//bg.scale.set(1.5);
bg.height = window.innerHeight;
bg.width = window.innerWidth;
app.stage.addChild(bg);


// --------- animated ghost ----------------------------
const cells = PIXI.Sprite.from('../images/Ghost Matter.jpg');

cells.scale.set(5);

const mask = PIXI.Sprite.from('../images/ooh.png');
mask.anchor.set(0.5);
mask.x = 310;
mask.y = 190;

cells.mask = mask;

app.stage.addChild(mask, cells);

const target = new PIXI.Point();

reset();

function reset() {
    target.x = Math.floor(Math.random() * app.renderer.width);
	target.y = Math.floor(Math.random() * app.renderer.height);
}

app.ticker.add(() => {
    mask.x += (target.x - mask.x) * 0.1;
    mask.y += (target.y - mask.y) * 0.1;

    if (Math.abs(mask.x - target.x) < 1) {
        reset();
    }
});






//--------------------------------BUTTONS----------------------------------
const passButton = PIXI.Sprite.fromImage('../images/pass.png');
passButton.x = 1200
passButton.y = 550
passButton.height = 90
passButton.width = 200 
app.stage.addChild(passButton);


const resignButton = PIXI.Sprite.fromImage('../images/resign.png');
resignButton.x = 1200
resignButton.y = 650
resignButton.height = 90
resignButton.width = 200 
app.stage.addChild(resignButton);

const soundButton = PIXI.Sprite.fromImage('../images/sound.png');
soundButton.x = 1400
soundButton.y = 10
soundButton.height = 90
soundButton.width = 90 
app.stage.addChild(soundButton);


const timerBoard = PIXI.Sprite.fromImage('../images/tim.png');
timerBoard.x = 1010
timerBoard.y = 130
timerBoard.height = 200
timerBoard.width = 500 
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
app.stage.addChild(countingText);

var tik = setInterval(animate , 1000);

//requestAnimationFrame(animate);
function animate()
{
    

        var min = Math.floor(seconds / 60);
        var remainSeconds = seconds % 60;
        if(seconds < 10 && seconds >0)
        {
            remainTime = "00 : "+ remainSeconds;
            seconds -= 1;
            
        }
        if(min < 10 && remainSeconds <10)
        {
            remainTime = "0" + min + " : 0"+remainSeconds; 
        }
        else if (seconds > 0)
        {
            
            remainTime = min + " : "+remainSeconds;
            seconds -= 1;
        }
        else
        {
            remainTime = "TIME OUT";
        }
        countingText.text = remainTime;

    
   // requestAnimationFrame(animate);
}
 

// ----------------------------------------------------------------------
const flexibility = 10;
const blockSz = 30;
const blockNum = 18;
const x = 450;
const y = 100;

var color = "black" //modify


const board = PIXI.Sprite.fromImage('../images/boardcartoon.png');
board.interactive = true;
margin =  30;
board.x = x - margin;
board.y = y - margin;
board.height = blockSz*blockNum + 2*margin;
board.width = blockSz*blockNum + 2*margin;

function inGrid(clickX, clickY){
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
    var clickPosX = event.data.global.x ;
    var clickPosY = event.data.global.y ;
    if(inGrid(clickPosX, clickPosY)){
        if(color === "white" )
            var stone = PIXI.Sprite.fromImage('../images/white.png');
        else
            var stone = PIXI.Sprite.fromImage('../images/black.png');
        
        clickPosX = Math.round(clickPosX / blockSz) * blockSz;
        clickPosY = Math.floor(clickPosY / blockSz) * blockSz;
        stone.x = clickPosX - blockSz/2;
        stone.y = clickPosY  ;
        stone.height = 25;
        stone.width = 25;
        app.stage.addChild(stone);
    }
 
};

board.on('pointerup', onClick);
app.stage.addChild(board);







//letters
var i;
var letterUp;
var letterDown;
var posX = x-5;
var posY = y;
var fontSz = 20;


for(i = 0; i<20; i++){
    if(String.fromCharCode(65+i) == "I") continue;
    const fontStyle = new PIXI.TextStyle({
        dropShadow: true,
        dropShadowAlpha: 0.4,
        dropShadowColor: "silver",
        //fontColor : 0x452000,
        fill: '#3e1707', 
        fontSize: fontSz ,
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
    app.stage.addChild(letterUp);
    app.stage.addChild(letterDown);
    posX += blockSz;
}

//numbers
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
    fontSize: fontSz ,
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

    app.stage.addChild(numLeft);
    app.stage.addChild(numRight);
    posY += blockSz;
}



var graphics = new PIXI.Graphics();
graphics.lineStyle(3, 0x000000, 1);

//modify to drawRect
graphics.drawPolygon([ x, y, 
                      blockSz*blockNum + x, y, 
                      blockSz*blockNum + x, blockSz*blockNum + y,
                      x, blockSz*blockNum + y,
                    ]);


var i;
var posX = x;
var posY = y;

//vertical lines
for (i = 0; i < blockNum; i++){
    posX += blockSz;
    graphics.moveTo(posX, y);
    graphics.lineTo(posX, blockSz*blockNum + y);
}

posX = x;
//horizontal lines
for (i = 0; i < blockNum; i++){
    posY += blockSz;
    graphics.moveTo(x, posY);
    graphics.lineTo(blockSz*blockNum + x, posY);
}

// Add the graphics to the stage
app.stage.addChild(graphics);




// Listen for window resize events
window.addEventListener('resize', resize);

// Resize function window
function resize() {
	// Resize the renderer
	app.renderer.resize(window.innerWidth, window.innerHeight);
}

resize();

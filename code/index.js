
const app = new PIXI.Application({
	autoResize: true,
  resolution: devicePixelRatio 
});

document.body.appendChild(app.view);
app.renderer.backgroundColor = 0xFFFFFF;

// Create the main stage for your display objects
var stage = new PIXI.Container();
stage.interactive = true;



const flexibility = 15;
const blockSz = 30;
const blockNum = 18;
const x = 450;
const y = 100;

var color = "black" //modify


const board = PIXI.Sprite.fromImage('./images/board.jpg');
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
    //if(clickXX < 0 || clickYY < 0) return false;
    //if(clickXX > blockNum*blockSz || clickYY > blockNum*blockSz) return false;
    //if(((clickXX + flexibility) % blockSz == 0 || (clickXX - flexibility) % blockSz == 0)  &&  ((clickYY + flexibility) % blockSz == 0 || (clickYY - flexibility) % blockSz == 0)) return true;
    return true;
}

function onClick(event){
    var clickPosX = event.data.global.x;
    var clickPosY = event.data.global.y;
    if(inGrid(clickPosX, clickPosY)){
        if(color === "white" )
            var stone = PIXI.Sprite.fromImage('./images/white.png');
        else
            var stone = PIXI.Sprite.fromImage('./images/black.png');

        stone.x = clickPosX - blockSz/2;
        stone.y = clickPosY - blockSz/2;
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
    letterUp = new PIXI.Text(String.fromCharCode(65+i),{fontSize: fontSz});
    letterDown = new PIXI.Text(String.fromCharCode(65+i),{fontSize: fontSz});
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

for(i = 19; i>0; i--){
    numLeft = new PIXI.Text(String(i),{fontSize: fontSz});
    numRight = new PIXI.Text(String(i),{fontSize: fontSz});
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
const interface = require("../interface.js");
const app = new PIXI.Application({
	autoResize: true,
  resolution: devicePixelRatio,
  width: 1080,
  height: 720
});

document.body.appendChild(app.view);
app.renderer.backgroundColor = 0x000000;

//////////////////////////////Mouse///////////////////////////////////
const defaultIcon = "url('../images/white.png'),auto";
const hoverIcon = "url('../images/black.png'),auto";
// Add custom cursor styles
app.renderer.plugins.interaction.cursorStyles.default = defaultIcon;
app.renderer.plugins.interaction.cursorStyles.hover = hoverIcon;
/////////////////////////////////////////////////////////////////////////
var stage = new PIXI.Container();
stage.interactive = true;

///////////////////////Background/////////////////////////
const texture = PIXI.Texture.from("../images/10.jpg");
const textureBlack = PIXI.Texture.from("../images/101.jpg");
var bg = PIXI.Sprite.fromImage(texture);
bg.scale.set(0.87);
app.stage.addChild(bg);

var interval = setInterval(ChangeBackground, 1000);
var black = 0;
function ChangeBackground(){

    if(!black) bg.texture = textureBlack;
    else bg.texture = texture;
    
    black = !black;
}
/////////////////////////Ghost//////////////////////////////////////////

const cells = PIXI.Sprite.from('../images/whitetexture.png');
cells.alpha = 0.5;
cells.scale.set(2.5);

const mask = PIXI.Sprite.from('../images/ghost@0,5x.png');
mask.anchor.set(0.5);
mask.scale.set(0.55);
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


//////////////////////////////////////Tail/////////////////////////////////////////////////////

// Get the texture for rope.
const trailTexture = PIXI.Texture.from('../images/trail.png');
const historyX = [];
const historyY = [];
// historySize determines how long the trail will be.
const historySize = 20;
// ropeSize determines how smooth the trail will be.
const ropeSize = 100;
const points = [];

// Create history array.
for (let i = 0; i < historySize; i++) {
    historyX.push(0);
    historyY.push(0);
}
// Create rope points.
for (let i = 0; i < ropeSize; i++) {
    points.push(new PIXI.Point(0, 0));
}

// Create the rope
const rope = new PIXI.SimpleRope(trailTexture, points);

// Set the blendmode
rope.blendmode = PIXI.BLEND_MODES.ADD;

app.stage.addChild(rope);

// Listen for animate update
app.ticker.add((delta) => {
    // Read mouse points, this could be done also in mousemove/touchmove update. For simplicity it is done here for now.
    // When implementing this properly, make sure to implement touchmove as interaction plugins mouse might not update on certain devices.
    const mouseposition = app.renderer.plugins.interaction.mouse.global;

    // Update the mouse values to history
    historyX.pop();
    historyX.unshift(mouseposition.x);
    historyY.pop();
    historyY.unshift(mouseposition.y);
    // Update the points to correspond with history.
    for (let i = 0; i < ropeSize; i++) {
        const p = points[i];

        // Smooth the curve with cubic interpolation to prevent sharp edges.
        const ix = cubicInterpolation(historyX, i / ropeSize * historySize);
        const iy = cubicInterpolation(historyY, i / ropeSize * historySize);

        p.x = ix;
        p.y = iy;
    }
});

function clipInput(k, arr) {
    if (k < 0) k = 0;
    if (k > arr.length - 1) k = arr.length - 1;
    return arr[k];
}

function getTangent(k, factor, array) {
    return factor * (clipInput(k + 1, array) - clipInput(k - 1, array)) / 2;
}

function cubicInterpolation(array, t, tangentFactor) {
    if (tangentFactor == null) tangentFactor = 1;

    const k = Math.floor(t);
    const m = [getTangent(k, tangentFactor, array), getTangent(k + 1, tangentFactor, array)];
    const p = [clipInput(k, array), clipInput(k + 1, array)];
    t -= k;
    const t2 = t * t;
    const t3 = t * t2;
    return (2 * t3 - 3 * t2 + 1) * p[0] + (t3 - 2 * t2 + t) * m[0] + (-2 * t3 + 3 * t2) * p[1] + (t3 - t2) * m[1];
}


////////////////////Button///////////////////
const distance = 1070;
const y =  window.innerHeight / 2 + 230;
const x = 100;

const blackButton = PIXI.Sprite.from('../images/blackbutton.png');
blackButton.scale.set(0.2);
blackButton.interactive = true;
blackButton.y = y;
blackButton.cursor = 'hover';
blackButton.x = x;
blackButton.on('click', function(){
    sessionStorage.setItem("color", "black");
    interface.send_opponent_color('0');
    location.assign("../html/index.html"); 
});
app.stage.addChild(blackButton);
//////////////////////////////
const whiteButton = PIXI.Sprite.from('../images/whitebutton.png');
whiteButton.scale.set(0.2);
whiteButton.interactive = true;
whiteButton.y = y;
//button2.cursor = 'hover';
whiteButton.x = x + distance;
whiteButton.on('click', function(){
    sessionStorage.setItem("color", "white");
    interface.send_opponent_color('1');
    location.assign("../html/index.html"); 
});
app.stage.addChild(whiteButton);
//////////////////////Text/////////////////////
var fontSz = 90;
const fontStyle = new PIXI.TextStyle({
    dropShadow: true,
    dropShadowAlpha: 0.4,
    dropShadowColor: "silver",
    //fontColor : 0x452000,
    fill: '#3e1707', 
    fontSize: fontSz ,
    fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
    fontStyle: "italic",
    fontWeight: "bold",stroke: '#a4410e', strokeThickness: 9
});

msg = new PIXI.Text("Choose Your Color",fontStyle);
msg.x = window.innerWidth/2-440;
msg.y = window.innerHeight/2 + 220;
app.stage.addChild(msg);

///////////////////////////////////////
// Listen for window resize events
window.addEventListener('resize', resize);

// Resize function window
function resize() {
	// Resize the renderer
	app.renderer.resize(window.innerWidth, window.innerHeight);
}

resize();


const interface = require("../interface.js");
const utilities = require("../js/utilities.js");
const app = new PIXI.Application({
	autoResize: true,
    resolution: devicePixelRatio,
});
document.body.appendChild(app.view);
app.renderer.backgroundColor = 0x000000;
var stage = new PIXI.Container();
stage.interactive = true;
//--------------------Mouse---------------------------
const defaultIcon = "url('../images/curserwhite.png'),auto";
const hoverIcon = "url('../images/cursorblack.png'),auto";
app.renderer.plugins.interaction.cursorStyles.default = defaultIcon;
app.renderer.plugins.interaction.cursorStyles.hover = hoverIcon;


var loader = new PIXI.Loader();
//Add all images
loader.add(["../images/startbglight.jpg", "../images/startbgblack.jpg", '../images/whitetexture.png',
            '../images/ghost@0,5x.png', '../images/trail.png', '../images/blackbutton.png',
             '../images/whitebutton.png', "../images/sound.png", "../images/mute.png"]);

loader.once('complete',setup);
loader.load();

function setup(){
    //---------------------------Background---------------------------
    const texture = PIXI.Texture.from("../images/startbglight.jpg");
    const textureBlack = PIXI.Texture.from("../images/startbgblack.jpg");
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
    //---------------------------Ghost---------------------------
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
    app.ticker.add(() => {
        mask.x += (target.x - mask.x) * 0.1;
        mask.y += (target.y - mask.y) * 0.1;

        if (Math.abs(mask.x - target.x) < 1) reset();
    });

    function reset() {
        target.x = Math.floor(Math.random() * app.renderer.width);
        target.y = Math.floor(Math.random() * app.renderer.height);
    }
    //---------------------------Buttons---------------------------
    const distance = 1070;
    const y =  window.innerHeight / 2 + 230;
    const x = 100;

    const blackButton = PIXI.Sprite.from('../images/blackbutton.png');
    blackButton.scale.set(0.2);
    blackButton.y = y;
    blackButton.x = x;

    const blackButtonRect = new PIXI.Graphics();
    blackButtonRect.lineStyle(1, 0xffffff);
    blackButtonRect.drawRect(130,window.innerHeight / 2 + 250, blackButton.width/2 + 30, blackButton.height/2);
    blackButtonRect.hitArea = new PIXI.Rectangle(130,window.innerHeight / 2 + 250, blackButton.width/2 + 30, blackButton.height/2);
    blackButtonRect.interactive = true;
    blackButtonRect.cursor = 'hover'

    blackButtonRect.on('click', function(){
        sessionStorage.setItem("color", "black");
        interface.send_opponent_color('0');
        location.assign("../html/main.html"); 
    });
    
    app.stage.addChild(blackButton);
    app.stage.addChild(blackButtonRect);
    
    const whiteButton = PIXI.Sprite.from('../images/whitebutton.png');
    whiteButton.scale.set(0.2);
    whiteButton.y = y;
    whiteButton.x = x + distance;

    const whiteButtonRect = new PIXI.Graphics();
    whiteButtonRect.lineStyle(1, 0xffffff);
    whiteButtonRect.drawRect(130+distance,window.innerHeight / 2 + 250, blackButton.width/2 + 30, blackButton.height/2);
    whiteButtonRect.hitArea = new PIXI.Rectangle(130+distance,window.innerHeight / 2 + 250,window.innerHeight / 2 + 250, blackButton.width/2 + 30, blackButton.height/2);
    whiteButtonRect.interactive = true;

    whiteButtonRect.on('click', function(){
        console.log("click white")
        sessionStorage.setItem("color", "white");
        interface.send_opponent_color('1');
        location.assign("../html/main.html"); 
    });
    app.stage.addChild(whiteButton);
    app.stage.addChild(whiteButtonRect);
    //---------------------------Text---------------------------
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

    utilities.addMouseTail(app);
    utilities.playSound()
}

// Listen for window resize events
window.addEventListener('resize', resize);
// Resize function window
function resize() {
	// Resize the renderer
	app.renderer.resize(window.innerWidth, window.innerHeight);
}
resize();


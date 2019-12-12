const interface = require("../interface.js");
const utilities = require("../js/utilities.js");
var sound = sessionStorage.getItem('sound');
const app = new PIXI.Application({
	autoResize: true,
    resolution: devicePixelRatio,
});
document.body.appendChild(app.view);
app.renderer.backgroundColor = 0xffffff;
var stage = new PIXI.Container();
app.stage.interactive = true;

var loader = new PIXI.Loader();
//Add all images
loader.add(["../images/AIVSAI.png", "../images/AIVSHUMAN.png", "../images/TRAINING.png",
            "../images/trail.png", "../images/sound.png", "../images/mute.png", '../images/dab.png']);
loader.once('complete',setup);
loader.load();

function setup(){
    const style = new PIXI.TextStyle({
        fontFamily: "\"Comic Sans MS\", cursive, sans-serif",
        dropShadow: true,
        dropShadowAlpha: 0.6,
        dropShadowColor: "silver",
        fill: '#3e1707', 
        fontSize : 170,
        align: 'center', 
        stroke: '#a4410e', strokeThickness: 10 
    });

    var ghost = "Ghost";
    var logoText = new PIXI.Text(ghost,style);
    logoText . x = 550;
    logoText.y = 120;
    app.stage.addChild(logoText);

    const logo = PIXI.Sprite.fromImage('../images/dab.png');
    logo.x = 300;
    logo.y = 100;
    logo.scale.set(0.5);
    app.stage.addChild(logo);

    const aiVsaiButton = PIXI.Sprite.from('../images/AIVSAI.png');
    aiVsaiButton.x = 80
    aiVsaiButton.y = 600
    aiVsaiButton.height = 120
    aiVsaiButton.width = 250 

    const aiVsaiButtonRect = new PIXI.Graphics();
    aiVsaiButtonRect.lineStyle(1, 0x000);
    aiVsaiButtonRect.drawRect(130,630, 150, 40);
    aiVsaiButtonRect.hitArea = new PIXI.Rectangle(130,630, 150, 40);
    aiVsaiButtonRect.interactive = true;
    aiVsaiButtonRect.buttonMode = true;
    
    aiVsaiButtonRect.on('click', function(event){
        console.log("clicked");
        sessionStorage.setItem("mode", "AIVSAI");
        interface.send_mode('1');
        location.assign("../html/main.html"); 
    
    });

    app.stage.addChild(aiVsaiButtonRect);
    app.stage.addChild(aiVsaiButton);
    
    
    const aiVshumanButton = PIXI.Sprite.fromImage('../images/AIVSHUMAN.png');
    aiVshumanButton.x = 1200
    aiVshumanButton.y = 600
    aiVshumanButton.height = 120
    aiVshumanButton.width = 250 

    const aiVshumanButtonRect = new PIXI.Graphics();
    aiVshumanButtonRect.lineStyle(1, 0x000);
    aiVshumanButtonRect.drawRect(1250,630, 150, 40);
    aiVshumanButtonRect.hitArea = new PIXI.Rectangle(1250,630, 150, 40);
    aiVshumanButtonRect.interactive = true;
    aiVshumanButtonRect.buttonMode = true;
    aiVshumanButtonRect.on('click', function(){
        sessionStorage.setItem("mode", "AIVSHuman");
        interface.send_mode('0');
        location.assign("../html/start.html"); 
    });
    app.stage.addChild(aiVshumanButtonRect);
    app.stage.addChild(aiVshumanButton);
    

    const trainingButton = PIXI.Sprite.fromImage('../images/TRAINING.png');
    trainingButton.x = 1200
    trainingButton.y = 600
    trainingButton.height = 120
    trainingButton.width = 250

    const trainingButtonRect = new PIXI.Graphics();
    trainingButtonRect.lineStyle(1, 0x000);
    trainingButtonRect.drawRect(1250,630, 150, 40);
    trainingButtonRect.hitArea = new PIXI.Rectangle(1250,630, 150, 40);
    trainingButtonRect.interactive = true;
    trainingButtonRect.buttonMode = true;

    trainingButtonRect.on('click', function(){
        sessionStorage.setItem("mode", "trainerTest");
        interface.send_mode('2');
        location.assign("../html/main.html"); 
    });
    
    //app.stage.addChild(trainingButtonRect);
    //app.stage.addChild(trainingButton);
    

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
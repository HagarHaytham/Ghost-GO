function addMouseTail(app){
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
}

function addSoundButton(app){
    const textureSound = PIXI.Texture.from("../images/sound.png");
    const textureMute = PIXI.Texture.from("../images/mute.png");
    var sound = true;
    var soundButton = PIXI.Sprite.fromImage(textureSound);
    soundButton.x = 1400
    soundButton.y = 10
    soundButton.height = 90
    soundButton.width = 90
    
    const soundButtonRect = new PIXI.Graphics();
    soundButtonRect.lineStyle(1, 0xffff);
    soundButtonRect.drawCircle (soundButton.x+soundButton.width/2, soundButton.y+soundButton.height/2, 30)
    soundButtonRect.hitArea = new PIXI.Circle(soundButton.x+soundButton.width/2, soundButton.y+soundButton.height/2, 30);
    soundButtonRect.interactive = true;
    soundButtonRect.buttonMode = true;

    soundButtonRect.on('click', function(){
       if(sound == true){
        soundButton.texture = textureMute;
       }
    
       else{
        soundButton.texture = textureSound;
       }
    
       sound = !sound;
    });
    app.stage.addChild(soundButton);
    app.stage.addChild(soundButtonRect);
}



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


module.exports = {addMouseTail, addSoundButton};
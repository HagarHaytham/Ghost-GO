(function() {
    /**
     * Setting Up Pixi.js
     */

    var renderer = PIXI.autoDetectRenderer(660, 500, {backgroundColor: 0xffffff});
    document.body.appendChild(renderer.view);
    renderer.backgroundColor = 0xffffff;
    // Create the stage
    var stage = new PIXI.Container();

    /**
     * Adding Some Basic Text
     */

    // Create a small arrow Text
    var arrowText = new PIXI.Text('>', {font: "bold 32px Roboto", fill: '#e74c3c'});

    // Set the anchor point in the center of the arrow
    arrowText.anchor.x = 0.5;
    arrowText.anchor.y = 0.5;

    // Position the arrow
    arrowText.x = 20;
    arrowText.y = 30;

    // Add arrow to stage
    stage.addChild(arrowText);

    // Create player one Text
    var playerOneText = new PIXI.Text('Player 1: 0');

    // Position the text
    playerOneText.x = 20;
    playerOneText.y = 15;

    // Add Player one Text to the stage
    stage.addChild(playerOneText);

    // Player Two Text
    var playerTwoText = new PIXI.Text('Player 2: 0');

    // Place the anchor at the top right corner of the text
    playerTwoText.anchor.x = 1;

    // Position the player two text at the same y position as player one
    // But with the x position at, full width (660) minus 20. (640)
    playerTwoText.x = renderer.width - 20;
    playerTwoText.y = 15;
    // Add player two text to the stage
    stage.addChild(playerTwoText);

    // Create the timer text
    var timerText = new PIXI.Text('00:00');

    // Place the anchor in the top center of the text
    timerText.anchor.x = 0.5;

    // Position the timer text at the top center of our stage
    timerText.x = renderer.width / 2;
    timerText.y = 15;

    // Add timer text to the stage
    stage.addChild(timerText);

    /**
     * Creating Some More Advanced Text
     */

    // Options for our "advanced" text
    var textOptions = {
        font: "bold 64px Roboto", // Set  style, size and font
        fill: '#3498db', // Set fill color to blue
        align: 'center', // Center align the text, since it's multiline
        stroke: '#34495e', // Set stroke color to a dark blue gray color
        strokeThickness: 20, // Set stroke thickness to 20
        lineJoin: 'round' // Set the lineJoin to round
    }

    // Create middleText with the textOptions. Use \n to make the line break
    var middleText = new PIXI.Text('Start Playing\nThe Game', textOptions);

    // Set anchor to the center of the text
    middleText.anchor.x = 0.5;
    middleText.anchor.y = 0.5;

    // Place text in the center of our stage
    middleText.x = renderer.width / 2;
    middleText.y = renderer.height / 2;

    // Add middleText to the stage
    stage.addChild(middleText);

    animate();

    function animate() {
        requestAnimationFrame(animate);

        // Make the arrowText move from left to right
        arrowText.position.x += 1;

        // Rotate the arrowText very quickly
        arrowText.rotation += 1;

        // If the arrow is at the end of the screen, place it at 0
        if (arrowText.position.x >= renderer.width) {
            arrowText.position.x = 0;
        }

        renderer.render(stage);
    }
})();

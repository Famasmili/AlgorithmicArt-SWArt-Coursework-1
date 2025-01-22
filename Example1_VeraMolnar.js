function settings() {
    h = 800
    w = 800
}

function setup() {
    colorMode = (HSB, 360, 100, 100, 250);
    createCanvas(h, w);
    stroke(0);
    strokeWeight(1);
    noFill();
    noLoop();
}

function draw() {
    background(0, 0, 0)
    stroke(0, 0, 100)
    noFill()
    rect(0, 0, w, h)
     stroke(0, 0, 0) // before was noStroke()
    fill(50, 100, 100)
    // rect(w*0.5, h*0.5, w*0.5, h*0.5)
    var size = w * 0.8
    var hsize = size * 0.5
    var vera = 42 // 21 after
    var molnar = 11 //
    var black = false
    for (i = 0; i < molnar; i++) {
        if(black){fill(50, 0, 0);black=false} // Draw in black if true
        else {fill(50, 100, 100);black=true} // Draw in yellow if false
        
        quad(w * 0.5 - hsize + random(-vera, vera),
            h * 0.5 - hsize + random(-vera, vera),
            w * 0.5 + hsize + random(-vera, vera),
            h * 0.5 - hsize + random(-vera, vera),
            w * 0.5 + hsize + random(-vera, vera),
            h * 0.5 + hsize + random(-vera, vera),
            w * 0.5 - hsize + random(-vera, vera),
            h * 0.5 + hsize + random(-vera, vera))
            hsize -= size * 0.05
    }
}
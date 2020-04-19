int size = 1;
JSONArray data;
int depth = 300;

void settings() {
    size(1080, 1080, P3D);
}

void setup() {
    noStroke();
    data = loadJSONArray("data.json");
    colorMode(HSB, 360);
    camera(width/2, height/2, depth, width/2, height/2, 0, 0, 1, 0);
}

float rx = 0;
float rz = 0;

void draw() {
    background(color(240, 100, 100));
    camera(width/2, height/2, depth, width/2, height/2, 0, 0, 1, 0);
    ambientLight(0, 0, 100, 0, 100, 0);
    directionalLight(0, 0, 80, 0, 50, -10);
    translate(width/2, height/2);
    rotateX(rz);
    rotateY(rx);
    display_region();
    rx += 0.005 * TWO_PI;
    saveFrame("data/frame####.png"); //Create gif 
    //ffmpeg -i %04d.png output.gif
}

void mouseDragged(){
    rx = map(mouseX, 0, width, -PI, PI);
    rz = map(mouseY, 0, width, PI, -PI);
    rx = constrain(rx, -PI, PI);
    rz = constrain(rz, -PI, PI);
}

// void mouseWheel(MouseEvent event) {
//   float e = event.getCount();
//   println(e);
// }

void mouseWheel(MouseEvent event) {
    depth += event.getCount() * 20;
}

void display_region() {
    for(int cx = 0; cx < 16; cx++) {
        for(int cz = 0; cz < 16; cz++) {
            for(int x = 0; x < 16; x++) {
                for(int z = 0; z < 16; z++) {
                    int index = x + z * 16 + cx * 16 * 16 + cz * 16 * 16 * 32;
                    if(!data.isNull(index)) {
                        JSONArray block = data.getJSONArray(index);
                        color c = color(block.getInt(0), block.getInt(1) * 3.6f, block.getInt(2) * 3 * 3.6f);
                        // if(c == color(60, 100 * 3.6f, 90 * 3 * 3.6f)) return;
                        int y = block.getInt(3);
                        pushMatrix();
                            translate((256/2 - x - cx * 16) * size, (256/2-y) * size, (256/2 - z - cz * 16) * size);
                            fill(c);
                            box(size);
                        popMatrix();
                    }
                }
            }
        }
    }
}

void display_chunk() {
    for(int x = 0; x < 16; x++) {
        for(int y = 0; y < 100; y++) {
            for(int z = 0; z < 16; z++) {
                int index = x + z * 16 + y * 256;
                if(!data.isNull(index)) {
                    JSONArray block = data.getJSONArray(index);
                    color c = color(block.getInt(0), block.getInt(1) * 3.6f, block.getInt(2) * 3 * 3.6f);
                    if(c == color(60, 100 * 3.6f, 90 * 3 * 3.6f)) return;
                    pushMatrix();
                        translate((16*size)/2 - x * size, (size * 100)/2 - y * size, (16*size)/2 - z * size);
                        fill(c);
                        box(4);
                    popMatrix();
                }
            }
        }
    }
}
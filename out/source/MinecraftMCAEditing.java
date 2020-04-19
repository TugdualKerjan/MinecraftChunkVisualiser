import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class MinecraftMCAEditing extends PApplet {

int size = 4;
JSONArray data;
int depth = 300;

public void settings() {
    size(1080, 1080, P3D);
}

public void setup() {
    noStroke();
    data = loadJSONArray("data.json");
    colorMode(HSB, 360);
    camera(width/2, height/2*0.35f, depth, width/2, height/2, 0, 0, 1, 0);
}

float rx = 0;
float rz = 0;

public void draw() {
    background(color(240, 100, 100));
    camera(width/2, height/2*0.35f, depth, width/2, height/2, 0, 0, 1, 0);
    ambientLight(0, 0, 100, 0, 100, 0);
    directionalLight(0, 0, 80, 0, 50, -10);
    translate(width/2, height/2);
    rotateX(rz);
    rotateY(rx);
    for(int x = 0; x < 16; x++) {
        for(int y = 0; y < 100; y++) {
            for(int z = 0; z < 16; z++) {
                display_block(x, y, z);
            }
        }
    }
    rx += 0.005f * TWO_PI;
    saveFrame("data/frame####.png");
}

public void mouseDragged(){
    rx = map(mouseX, 0, width, -PI, PI);
    rz = map(mouseY, 0, width, PI, -PI);
    rx = constrain(rx, -PI, PI);
    rz = constrain(rz, -PI, PI);
}

// void mouseWheel(MouseEvent event) {
//   float e = event.getCount();
//   println(e);
// }

public void mouseWheel(MouseEvent event) {
    depth += event.getCount() * 20;
}

public void display_block(int x, int y, int z) {
    int index = x + z * 16 + y * 256;
    if(!data.isNull(index)) {
        JSONArray block = data.getJSONArray(index);
        int c = color(block.getInt(0), block.getInt(1) * 3.6f, block.getInt(2) * 3 * 3.6f);
        if(c == color(60, 100 * 3.6f, 90 * 3 * 3.6f)) return;
        pushMatrix();
            translate((16*size)/2 - x * size, (size * 100)/2 - y * size, (16*size)/2 - z * size);
            fill(c);
            box(4);
        popMatrix();
    }
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "MinecraftMCAEditing" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}

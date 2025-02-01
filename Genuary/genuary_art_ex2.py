import turtle
import random
import colorsys
import math

# Global variables
num_layers = 50
sides = random.choice([1, 3, 4, 5, 6, 7, 8, 9, 10])
length = 50
height = 800
width = 800
rotation_speed = 2  # Degrees per frame
rotate = True
rotation_direction = 1
frame_count = 0
colors_list = []
#direction = random.choice([0, 1]) # Random initial direction

class Polygon:
    def __init__(self, turtle, sides=3, length=10, color="black"):
        self.turtle = turtle
        self.sides = sides
        self.length = length
        self.color = color

    def draw(self, color=None):
        if color:
            self.turtle.color(color)
        self.turtle.color(self.color)
        for _ in range(self.sides):
            self.turtle.forward(self.length)
            self.turtle.right(360 / self.sides)

def setup(turtle):
    turtle.screen.setup(width, height)
    turtle.screen.title("Layers upon layers upon layers")
    turtle.screen.bgcolor("black")
    turtle.screen.tracer(0, 0)
    turtle.speed(0)
    turtle.hideturtle()

def draw_layer(t, polygon, layer_index, rotation_direction):
    # Diagonal position of the layer from top left to bottom right
    x_offset = -width // 2 +(layer_index * width // num_layers)
    y_offset = -height // 2 + (layer_index * height // num_layers)
    
    t.penup()
    t.goto(x_offset, y_offset)
    t.pendown()
    # t.setheading(t.heading() + rotation_direction)
    polygon.draw()

def rotation(x, y):
    global rotate
    rotate = not rotate

def inverse_rotation():
    global rotation_speed
    rotation_speed *= -1

# def change_color(x, y):
#     global color_change
#     color_change = not color_change

def color_shuffle():
    global colors_list
    
    if len(colors_list) < num_layers:
        for i in range(num_layers - len(colors_list)):
            hue = (math.sin((frame_count + i) * 0.02) * 0.5) + 0.5
            colors_list.append(colorsys.hsv_to_rgb(hue, 1.0, 1.0))
    random.shuffle(colors_list)
    shuffled_copy = colors_list.copy()
    for i in range(num_layers):
        colors_list[i] = shuffled_copy[i]

    turtle.update()

def animate():
    global rotate, frame_count, t, t1, colors_list, rotation_direction
    amplitude = 0.5 # Color change amplitude
    frequency = 0.02 # Color change frequency
    
    # Main loop
    while hasattr(turtle.Screen(), "_root") and turtle.Screen()._root is not None:
        frame_count += 1
        
        try:
            if t.screen._root is None or t1.screen._root is None:
                break
            t.clear()
            t1.clear()
        except turtle.TurtleGraphicsError:
            print("Turtle graphic window may have been closed.")
            break
        
        if rotate:
            t.setheading(t.heading() + rotation_speed * rotation_direction)
            t1.setheading(t1.heading() - rotation_speed * rotation_direction)
        
        for i in range(num_layers):
            if len(colors_list) < num_layers:
                hue = (math.sin((frame_count + i) * frequency) * amplitude) + 0.5
                colors_list.append(colorsys.hsv_to_rgb(hue, 1.0, 1.0))
            else:
                hue_shift = math.sin((frame_count + i) * frequency) * amplitude + 0.5
                new_color = colorsys.hsv_to_rgb(hue_shift, 1.0, 1.0)
                blend_factor = 0.1
                colors_list[i] = (
                    colors_list[i][0] * (1 - blend_factor) + new_color[0] * blend_factor,
                    colors_list[i][1] * (1 - blend_factor) + new_color[1] * blend_factor,
                    colors_list[i][2] * (1 - blend_factor) + new_color[2] * blend_factor,
                )
            color = colors_list[i]
            t.color(color)
            t1.color(color)

            side_length = length - 3 * i
            if sides == 1:
                t.penup() # Pull the pen up, no drawing done when moving the turtle around the canvas
                t.goto(0,0)
                t.pendown() # Put the pen down
                t.circle(side_length)
                t1.penup()
                t1.goto(0,0)
                t1.pendown()
                t1.circle(-side_length) 
            else:
                polygon = Polygon(t, sides, side_length, color)
                polygon1 = Polygon(t1, sides, side_length, color)
                draw_layer(t, polygon, i, rotation_direction)
                draw_layer(t1, polygon1, num_layers - i - 1, -rotation_direction)
        
        turtle.update()
        turtle.time.sleep(0.02)  # Sleep for 20ms

def main():
    global t, t1
    t = turtle.Turtle()
    t1 = turtle.Turtle()
    t.width(3)
    t1.width(3)
    setup(t)
    setup(t1)

    print(f"sides: {sides}")
    turtle.onscreenclick(rotation, btn=1) # When the screen is clicked(left-click), control rotation
    
    turtle.onkey(inverse_rotation, "i")
    turtle.onkey(color_shuffle, "s")
    turtle.listen()
    
    animate() # Begin the animation
    turtle.done()

if __name__ == "__main__":
    main()
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
    frame_count += 1
    amplitude = 0.5 # Color change amplitude
    frequency = 0.02 # Color change frequency
    
    # if not turtle.Screen()._root or not t.screen or not t1.screen:
    #     print("Turtle graphic window may have been closed.")
    #     return
    if not hasattr(turtle.Screen(), "_root") or turtle.Screen()._root is None:
        return 

    try:
        t.clear()
        t1.clear()
    except turtle.TurtleGraphicsError:
        print("Turtle graphic window may have been closed.")
        return
    
    if rotate:
        t.setheading(t.heading() + rotation_speed * rotation_direction)
        t1.setheading(t1.heading() - rotation_speed * rotation_direction)
    
    if len(colors_list) < num_layers:
        for i in range(num_layers):
            hue = (math.sin((frame_count + i) * frequency) * amplitude) + 0.5
            colors_list.append(colorsys.hsv_to_rgb(hue, 1.0, 1.0))
    else:
        for i in range(num_layers):
            hue = (math.sin((frame_count + i) * frequency) * amplitude) + 0.5
            colors_list[i] = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    for i in range(num_layers):
        color = colors_list[i]
        # color = (color[0], color[1], color[2])
        t.color(color)
        t1.color(color)

        side_length = length - 3 * i
        # rotation_direction = rotation_speed if i % 2 == 0 else -rotation_speed
        # Draw on both sides of the origin
        if sides == 1:
            # t.setheading(t.heading() + rotation_direction)
            t.penup()
            t.goto(0,0)
            t.pendown()
            t.circle(side_length)
            # t1.setheading(t1.heading() - rotation_direction)
            t1.penup()
            t1.goto(0,0)
            t1.pendown()
            t1.circle(-side_length) 
        else:
            polygon = Polygon(t, sides, side_length, color)
            polygon1 = Polygon(t1, sides, side_length, color)
            # Draw on both sides of the origin along the diagonal from top left to bottom right
            draw_layer(t, polygon, i, rotation_direction)
            draw_layer(t1, polygon1, num_layers - i - 1, -rotation_direction)
            # Draw on both sides of the origin along the diagonal from top right to bottom left
            # draw_layer(t, polygon, width / 4, height - 10 * i, rotation_direction)
            # draw_layer(t1, polygon1, -width / 4 + 10 * i, -300 + 10 * i, -rotation_direction)
            # draw_layer(t, polygon, width / 4, 300 - 10 * i, rotation_direction)
            # draw_layer(t1, polygon1, -width / 4 + 10 * i, -height + 10 * i, -rotation_direction)

    turtle.update()
    turtle.Screen().ontimer(animate, 20) # call this function again after 20ms

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
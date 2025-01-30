"""
This piece is inspired by the Genuary prompt "Layers upon layers upon layers" from Jan. 2.
It is a simple piece that creates a series of polygons that are layered on top of each other.
We pick the number of sides of the polygon, the color of each polygon, and the length of the sides.
The polygons are drawn in a spiral pattern, with each polygon being slightly larger than the previous one.


"""

import turtle
import random
import colorsys

####################################################################################################
# Genuary Art Exercise 1
####################################################################################################

# Global variables
num_layers = 50
sides = random.choice([1, 3, 4, 5, 6, 7, 8, 9, 10])
length = 200
height = 800
width = 800

class Polygon:
    def __init__(self, turtle, sides=1, length=10, color="black"):
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
            self.turtle.right(360/self.sides)

def setup(turtle):
    turtle.screen.setup(width, height)
    turtle.screen.title("Layers upon layers upon layers")
    turtle.screen.bgcolor("black")
    turtle.screen.tracer(0, 0)

    turtle.speed(0)
    #turtle.hideturtle()
    

def main():
    t = turtle.Turtle()
    setup(t)
    print(f"Number of layers: {num_layers}")
    print(f"Number of sides: {sides}")
    t.penup()
    t.goto(0, 300)
    t.pendown()
    for i in range(num_layers):
        color = colorsys.hsv_to_rgb(i/num_layers, 1.0, 1.0) # Generate a color based on the HSV color space
        color = (color[0], color[1], color[2])
        side_length = length - 3 * i

        if sides == 1:
            t.circle(side_length)
        else:
            p = Polygon(t, sides, side_length, color)
            p.draw()
        t.penup()
        new_y = t.ycor() - 10
        
        t.goto(t.xcor(), new_y) # Move the turtle up from its current position
        t.pendown()
        #if t.pos() > (width/2, height/2):
            

         
        

    turtle.update()
    turtle.done()

if __name__ == "__main__":
    main()
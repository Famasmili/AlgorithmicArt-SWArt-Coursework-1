import turtle
from random import random, seed, choice, randint
#from noise import pnoise2

"""
This is a spiral pattern generator using the turtle module.
The turtle moves forward and turns right by a random angle.
The distance between the lines is increased by 1 at each iteration.
The number of lines to draw is set to 200, but can be modified.
The inspiration for this code comes from the following link: https://www.youtube.com/shorts/uglTZY484I8?si=zsd0j7TEZbuCxjYo
The name of the Youtube channel is "Elastic Tech Days".

"""

# Set the seed for the random number generator
#seed(0)

# Set up the turtle
def setup():
    turtle.setup(1000, 1000)
    turtle.bgcolor("black")
    turtle.color("white")
    turtle.width(2)
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(-400, 400)
    turtle.pendown()

def fade_away():
    for i in range(10):
        t.color(turtle_color, "")
        t.shapesize(outline=10-i)
        t.screen.update()
        t.screen.delay(100)

def rotate():
    for i in range(36):
        t.right(10)
        t.screen.update()
        t.screen.delay(100)

def translate():
    for i in range(200):
        t.penup()
        t.forward(5)
        t.pendown()
        t.screen.update()
        t.screen.delay(100)

t = turtle.Turtle()
setup()

# Set the size of the screen
#t.screen.setup(1000, 1000)

# Set the speed of the turtle
t.speed(0) # 0 is the fastest speed, 1 is slowest, 10 is the default

# Set the color of the turtle
#t.screen.bgcolor("black")
#t.color("black")
turtle_color = choice(["red", "green", "blue", "purple", "yellow", "orange", "grey", "pink", "cyan", "magenta"])
t.color(turtle_color)

# Set the width of the turtle
t.width(randint(1, 5))
#t.width(2)

# Set the initial position of the turtle
#t.penup()
#t.goto(-400, -400) # Lower left corner

dist = 1 # Initial distance between the lines
flag = 200 # Number of lines to draw
angles = choice([30, 45, 60, 90, 120, 150, 240])
print("Color: " + turtle_color + " Angle: " + str(angles))
while flag > 0:

    t.begin_poly()
    t.color(turtle_color, "white")
    t.begin_fill()
    
    t.forward(dist)
    t.right(angles) # Random angle
    t.right(1)
    dist += 2 # Increase the distance between the lines
    flag -= 1 # Avoid infinite loop
    t.end_poly()
    t.end_fill()
    polygone = t.get_poly() # Get the polygon
    t.screen.addshape("polygone", polygone) # Add the polygon to the screen
    t.screen.onkey(fade_away, "f")
    t.screen.onkey(rotate, "r")
    t.screen.onkey(translate, "t")
    t.screen.listen()
    t.screen.update()
    #fade_away()
    #rotate()
    #translate()
    
t.onclick(t.shape("polygone"),btn=1) # Set the shape of the turtle to the polygon
# Set the title of the screen
turtle.title("Spiralling Patterns")

t.penup()
t.color("white")
t.goto(-200, -200) # Upper left corner
t.pendown()
turtle.write("Color: " + turtle_color + " Angle: " + str(angles), font=("Arial", 12, "normal"), align="center")


# Hide the turtle
t.hideturtle()

# Display the screen
turtle.mainloop()
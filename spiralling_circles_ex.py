import turtle
from random import seed
from noise import pnoise2

# Set the seed for the random number generator
seed(0)

# Set the size of the screen
t = turtle.Turtle()

# Set the size of the screen
t.screen.setup(800, 800)

# Set the speed of the turtle
t.speed(0)

# Set the color of the turtle
t.color("black")

# Set the width of the turtle
t.width(2)

# Set the initial position of the turtle
#t.penup()
#t.goto(-400, -400) # Lower left corner

dist = 1 # Initial distance between the lines
flag = 200 # Number of lines to draw

while flag:
    t.forward(dist)
    t.right(120)
    t.right(1)
    dist += 1 # Increase the distance between the lines
    flag -= 1 # Avoid infinite loop

# Hide the turtle
t.hideturtle()

# Display the screen
turtle.done()
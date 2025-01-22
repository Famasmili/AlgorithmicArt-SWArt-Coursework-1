import turtle
from random import random, seed, choice, randint
#from noise import pnoise2

"""
This is a spiral pattern generator using the turtle module.
The turtle moves forward and turns right by a random angle.
The distance between the lines is increased by 1 at each iteration.
The number of lines to draw is set to 500, but can be modified.
The inspiration for this code comes from the following link: https://www.youtube.com/shorts/uglTZY484I8?si=zsd0j7TEZbuCxjYo
The name of the Youtube channel is "Elastic Tech Days".

"""

# Set the seed for the random number generator
seed(0)

# Set the size of the screen
t = turtle.Turtle()

# Set the size of the screen
t.screen.setup(800, 800)

# Set the speed of the turtle
t.speed(2) # 0 is the fastest speed, 1 is slowest, 10 is the default

# Set the color of the turtle
#t.color("black")
t.color(choice(["red", "green", "blue", "purple", "black"]))

# Set the width of the turtle
t.width(randint(1, 5))
#t.width(2)

# Set the initial position of the turtle
#t.penup()
#t.goto(-400, -400) # Lower left corner

dist = 1 # Initial distance between the lines
flag = 200 # Number of lines to draw
angles = [30, 45, 60, 90, 120, 150, 240]

while flag:
    t.forward(dist)
    t.right(choice(angles)) # Random angle
    t.right(2)
    dist += 1 # Increase the distance between the lines
    flag -= 1 # Avoid infinite loop

# Hide the turtle
t.hideturtle()

# Display the screen
turtle.mainloop()
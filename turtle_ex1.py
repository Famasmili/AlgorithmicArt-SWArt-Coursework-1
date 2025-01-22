from turtle import *
from random import random, seed


random()
seed(42)
"""Basics"""

# Set color and pen width for the turtle
color('red', 'yellow')
width(8)

# Draw a triangle, play around with the angles and directions
forward(100)
backward(100)
left(120)
forward(100)
left(120)
forward(100)
pos() # Get the current position of the turtle
print(pos())
home() # Move the turtle to the origin(0,0)
#clearscreen() # Clear the screen and move the turtle to the origin

done() # Finish the turtle graphics, keep the window open
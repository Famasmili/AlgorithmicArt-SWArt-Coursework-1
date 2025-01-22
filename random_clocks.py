import turtle
import random
import time

# Set up the screen
wn = turtle.Screen()
wn.title("Random Clocks")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0) # Stops the window from updating
random.seed(42)

# Create the clock
clock = turtle.Turtle()
clock.speed(0)
clock.color("white")
clock.shape("circle")
clock.shapesize(stretch_wid=3, stretch_len=3) # Make the clock bigger
clock.penup()
# Create the hour hand
hour_hand = turtle.Turtle()
hour_hand.speed(0)
hour_hand.color("white")
hour_hand.shape("triangle")
hour_hand.shapesize(stretch_wid=0.5, stretch_len=5)
hour_hand.penup()

# Create the minute hand
minute_hand = turtle.Turtle()
minute_hand.speed(0)
minute_hand.color("white")
minute_hand.shape("triangle")
turtle.done()

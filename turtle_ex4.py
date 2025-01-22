from turtle import *
from random import random, seed

seed(42)  # Seed the random number generator to get the same results every time

# Draw something randomly, introduce some randomness in the movement
for steps in range(100):
    distance = random() * 100
    angle = random() * 360  
    right(angle)
    forward(distance)
    print(pos())
    print(heading())
    print(distance)
    print(angle)
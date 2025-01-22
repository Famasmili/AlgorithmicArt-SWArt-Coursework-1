from turtle import *
from random import random, seed

seed(0)

# Set up the screen
def grid(n, m, size):
    for i in range(n):
        for j in range(m):
            x = i * size
            y = j * size
            penup()
            goto(x, y)
            pendown()
            for _ in range(4):
                forward(size)
                right(90)
    penup()
    goto(0, 0)
    pendown()

# Draw a grid
grid(10, 10, 20)
mainloop()
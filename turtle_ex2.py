from turtle import *


# Draw something more complex using an algorithm
for steps in range(100):
    for c in ('blue', 'red', 'green'):
        color(c)
        forward(steps)
        left(90)

# Keep the window open
mainloop()
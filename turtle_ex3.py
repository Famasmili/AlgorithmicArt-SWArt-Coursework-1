from turtle import *

# Draw a star, specifically the one on the official turtle documentation page
color('red')
fillcolor('yellow')

begin_fill()
while True:
    forward(200)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()

mainloop()
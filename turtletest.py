import turtle
import PyQt5 #in case we find a way to use it
import tkinter as tk #apparently turtles only really works with tkinter
import random

# I'm assuming we're just going to be using square-shaped grid spaces
rolumns = 4 # rolumns = rows & columns
dimension = 1000 # the total height and length of grid 
halfdimension = dimension/2
boxwidth = dimension/rolumns
ui_offset = 100
#creating a nested list for referring to grid turtles' positions
pos = []
ypos = []
#grid turtles will simply "spawn" the functioning turtles at their locations
gridturtles = []
occupiedspace = []
activeturtles = [] #list of dictionaries to represent active turtles with attributes
					#let me know if there's a better method of doing this, and I'll
					#try to make the adjustment (to spare you from dealing with my messy code)

def randomspawn():
	if (int(spawn_input.get()) > len(gridturtles)):
		print("cannot spawn that many turtles")
	else:
		for i in range(int(spawn_input.get())):
			randomx = random.randrange(len(pos)) #probably could've just used rolumns, 
			randomy = random.randrange(len(pos[randomx])) #but wanted to be prepared for any circumstance
			#if the grid space is already taken by an active turtle, tries generating another coordinate pair
			if (f"{randomx}, {randomy}" in occupiedspace):
				randomspawnonce()
			else:
				gridturtle = pos[randomx][randomy]
				newturtle = gridturtle.clone()
				newturtle.showturtle()
				occupiedspace.append(f"{randomx}, {randomy}")
				turtleinfo = {	'object': newturtle, 
								'currentpos': f'{randomx}, {randomy}'}
				activeturtles.append(turtleinfo)
def randomspawnonce():
	randomx = random.randrange(len(pos))  
	randomy = random.randrange(len(pos[randomx])) 	
	if (f"{randomx}, {randomy}" in occupiedspace):
			randomspawnonce()
	else:
		gridturtle = pos[randomx][randomy]
		newturtle = gridturtle.clone()
		newturtle.showturtle()
		occupiedspace.append(f"{randomx}, {randomy}")
		turtleinfo = {	'object': newturtle, 
						'currentpos': f'{randomx}, {randomy}'}
		activeturtles.append(turtleinfo)
def press():
    do_stuff()


if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(1560, 1080)
    screen.bgcolor("white")
    canvas = screen.getcanvas()
    button = tk.Button(canvas.master, text="Randomly Spawn", command=randomspawn)
    canvas.create_window(-halfdimension-ui_offset, -halfdimension+3*ui_offset, window=button)
    spawn_input = tk.Entry()
    spawnamount = spawn_input.get()
    canvas.create_window(-halfdimension-ui_offset, -halfdimension+4*ui_offset, window=spawn_input)
    

t = turtle.Turtle()
t.hideturtle()
t.speed(100000)
t.penup()
t.goto(-halfdimension,-halfdimension) #bottom left corner
t.pendown()

#draws the outer bounds
for i in range(4):
	t.fd(dimension)
	t.lt(90)
#draws the grid lines
for i in range(rolumns):
	t.penup()
	t.setpos(-halfdimension ,-halfdimension + i*(boxwidth))
	t.pendown()
	t.fd(dimension)
	t.rt(90)
	t.penup()
	t.setpos(-halfdimension + i*(boxwidth),halfdimension)
	t.pendown()
	t.fd(dimension)
	t.lt(90)
t.penup()
#creates a new turtle clone each column down and adds them to the list
for a in range(rolumns):
	t.setpos(-halfdimension + (.5 + a)*(boxwidth), 
			halfdimension - .5*(boxwidth))
	for b in range(rolumns):
		t.sety(halfdimension - (.5 + b)*(boxwidth))
		ypos.append(t.clone())
		gridturtles.append(t.clone())
	pos.append(ypos)
	ypos = []

turtle.done()

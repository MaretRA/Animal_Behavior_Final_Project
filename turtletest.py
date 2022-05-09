import turtle
import PyQt5 #in case we find a way to use it
import tkinter as tk #apparently turtles only really works with tkinter
import random
from tkinter import *
import numpy
import matplotlib.pyplot as plot

# I'm assuming we're just going to be using square-shaped grid spaces
rolumns = 10 # rolumns = rows & columns
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
	if (state.get() == "Ready to Spawn"):
		state.set("Spawning")
		if (int(spawn_input.get()) > (len(gridturtles)-len(activeturtles))):
			message.set('Spawn failed: \n Too little space / Loading')
		else:
			for i in range(int(spawn_input.get())):
				randomspawnonce()
		#population_size['text'] = f'{len(activeturtles)}'
		population.set(f'{len(activeturtles)}')
		state.set("Ready to Spawn")
	else:
		message.set('Wait for the "Ready" State')
#		plot_cont()

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
def makemodule(coefficientx, coefficienty, module):
	canvas.create_window(-halfdimension-(1+coefficientx)*ui_offset, 
		-halfdimension+coefficienty*ui_offset, window =module)

if __name__ == "__main__":
    screen = turtle.Screen()
    screen.title("Simulation")
    screen.setup(1560, 1080)
    screen.bgcolor("white")
    canvas = screen.getcanvas()

    button = tk.Button(canvas.master, text="Randomly Spawn", command=randomspawn)
    spawn_input = tk.Scale(canvas.master, from_ = len(gridturtles), orient=HORIZONTAL)
    spawnamount = spawn_input.get()
    population = tk.StringVar(canvas.master, '0')
    population_size = tk.Label (canvas.master, textvariable =population)
    state = tk.StringVar(canvas.master, 'Loading')
    simulationstate = tk.Label (canvas.master, textvariable =state)
    message = tk.StringVar(canvas.master, 'Welcome to the simulation! \n Start by spawning turtles')
    systemmessage = tk.Label (canvas.master, textvariable =message)

    populationtext = tk.StringVar(canvas.master, 'Number of turtles')
    populationlabel = tk.Label (canvas.master, textvariable = populationtext)
    statetext = tk.StringVar(canvas.master, 'Current State')
    statelabel = tk.Label (canvas.master, textvariable = statetext)
    inputtext = tk.StringVar(canvas.master, 'Number of Turtles\n to Add')
    inputlabel = tk.Label (canvas.master, textvariable = inputtext)
    messagelabeltext = tk.StringVar(canvas.master, 'Console')
    messagelabel = tk.Label (canvas.master, textvariable = messagelabeltext)

    makemodule(0, 2.6, button)
    makemodule(0, 2.2, spawn_input)
    makemodule(0, 3.1, population_size)
    makemodule(0, 1.6, simulationstate)
    makemodule(1.25, 3, populationlabel)
    makemodule(1.25, 1.5, statelabel)
    makemodule(0, .85, systemmessage)
    makemodule(1.25, 2.1, inputlabel)
    makemodule(1.25, .75, messagelabel)

#y = []
#def plot_cont():
#    fig = plot.figure()
#    ax = fig.add_subplot(1,1,1)
#
#    def update(i):
#        yi = len(activeturtles)
#        y.append(yi)
#        x = range(len(y))
 #       ax.clear()
#        ax.plot(x, y)
#
#    a = anim.FuncAnimation(fig, update)
#    plot.show()

state.set('Creating Grid')
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


state.set("Ready to Spawn")

turtle.done()

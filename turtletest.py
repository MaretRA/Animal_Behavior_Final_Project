import turtle

t = turtle.Turtle()
s = turtle.Screen()

# I'm assuming we're just going to be using square-shaped grid spaces
rolumns = 10 # rolumns = rows & columns
dimension = 1000 # the total height and length of grid 
halfdimension = dimension/2

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
	t.setpos(-halfdimension ,-halfdimension + i*(dimension/rolumns))
	t.pendown()
	t.fd(dimension)
	t.rt(90)
	t.penup()
	t.setpos(-halfdimension + i*(dimension/rolumns),halfdimension)
	t.pendown()
	t.fd(dimension)
	t.lt(90)
#creating a nested list for referring to turtles' positions
turtles = []
turtlesy = []
t.penup()
#creates a new turtle clone each column down and adds them to the list
for a in range(rolumns):
	t.setpos(-halfdimension + (.5 + a)*(dimension/rolumns), 
			halfdimension - .5*(dimension/rolumns))
	for b in range(rolumns):
		t.sety(halfdimension - (.5 + b)*(dimension/rolumns))
		turtlesy.append(t.clone())
	turtles.append(turtlesy)
	turtlesy = []
print(turtles[0][0])

turtle.done()

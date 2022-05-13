from random import randrange
import turtle
from turtle import Shape
import tkinter as tk
import random
from tkinter import *
import math


rolumns = 20 # rolumns = rows & columns
dimension = 1000 # the total height and length of grid 
halfdimension = dimension/2
boxwidth = dimension/rolumns
ui_offset = 100
graphorigin = (halfdimension + .6* ui_offset, halfdimension - 4*ui_offset)
mimicgraphorigin = (halfdimension + .6*ui_offset, -halfdimension + .5*ui_offset)
axislength = 350
pos = []
gridturtles = [] 


# sets up width, height, and array
width = 20
height = 20

array = []
for i in range(width):
    array.append([])
    for j in range(height):
        array[i].append([])

# array = [[[]] * height] * width

# debug
# print("array:")
# print(array)
# print("\n\n")
# print(len(array))
# print(len(array[0]))


# creates lists of all animals
list_of_coral_snakes = []
list_of_king_snakes = []
list_of_bull_frogs = []

def get_width():
    return width

def get_height():
    return height

def makemodule(coefficientx, coefficienty, module):
    screen = turtle.Screen()
    canvas = screen.getcanvas()
    canvas.create_window(-halfdimension-(1+coefficientx)*ui_offset, 
        -halfdimension+coefficienty*ui_offset, window =module)

def updatedisplay(generationnumber):
    cspop.set(len(list_of_coral_snakes))
    kspop.set(len(list_of_king_snakes))
    bfpop.set(len(list_of_bull_frogs))
    generation.set(generationnumber)
def updategraph(generationnumber):
    cslastposition = cstracer.pos()[0]
    kslastposition = kstracer.pos()[0]
    bflastposition = bftracer.pos()[0]
    mimiclastposition = mimictracer.pos()[0]
    xincrement = axislength/generations_input.get()
    cstracer.goto(cslastposition + xincrement, graphorigin[1] + len(list_of_coral_snakes))
    kstracer.goto(kslastposition + xincrement, graphorigin[1] + len(list_of_king_snakes))
    bftracer.goto(bflastposition + xincrement, graphorigin[1] + len(list_of_bull_frogs))
    mimictracer.pencolor(100+int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*1.5)), 
    100-int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*1)),
    200-int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*2)))
    if (1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes)-20) > 0:
        mimictracer.goto(mimiclastposition + xincrement, mimicgraphorigin[1] + (1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes)-20)*4.5)
    else:
        mimictracer.goto(mimiclastposition + xincrement, mimicgraphorigin[1])

def startsimulation():
    if state.get() == "Ready to Simulate":
        disable()
        generationnumber = 0
        maxgeneration.set(generations_input.get())
        state.set("Spawning")
        possible_starting_locations = []
        for i in range(get_width()):
            for j in range(get_height()):
                possible_starting_locations.append([i,j])
        
        if coralsnake_input.get() + kingsnake_input.get() + bullfrog_input.get() > len(possible_starting_locations):
            message.set("Error, more animals than starting locations.")
            state.set("Done Simulating.")
            return "Error, more animals than starting locations."
        
        # adds the coral_snakes
        for cs in range(coralsnake_input.get()):
            ind = randrange(len(possible_starting_locations))
            indices = possible_starting_locations[ind]
            # prints indices for debugging purposes.
            #print("indices[0] = %s, indices[1] = %s" % (indices[0], indices[1]))
            list_of_coral_snakes.append(Coral_Snake(indices[0], indices[1], rounds_survived=randrange(4)))
            del possible_starting_locations[ind]
        
        # adds the king snakes
        for ks in range(kingsnake_input.get()):
            ind = randrange(len(possible_starting_locations))
            indices = possible_starting_locations[ind]
            list_of_king_snakes.append(King_Snake(indices[0], indices[1], rounds_survived=randrange(4)))
            del possible_starting_locations[ind]

        # adds the bullfrogs
        for bf in range(bullfrog_input.get()):
            ind =randrange(len(possible_starting_locations))
            indices = possible_starting_locations[ind]
            list_of_bull_frogs.append(Bull_Frog(indices[0], indices[1], rounds_survived=randrange(4)))
            del possible_starting_locations[ind]

        state.set("Simulating...")
        updatedisplay(generationnumber)
        cstracer.goto(graphorigin[0], graphorigin[1] + len(list_of_coral_snakes))
        kstracer.goto(graphorigin[0], graphorigin[1] + len(list_of_king_snakes))
        bftracer.goto(graphorigin[0], graphorigin[1] + len(list_of_bull_frogs))
        mimictracer.goto(mimicgraphorigin[0], mimicgraphorigin[1])
        cstracer.pendown()
        kstracer.pendown()
        bftracer.pendown()
        mimictracer.pendown()

        for i in range(generations_input.get()):
            generationnumber = generationnumber + 1
            game_round()
            updatedisplay(generationnumber)
            updategraph(generationnumber)
            print("Number of coral snakes: %s" % len(list_of_coral_snakes))
            print("Number of king snakes: %s" % len(list_of_king_snakes))
            print("Number of bullfrogs: %s" % len(list_of_bull_frogs))
            print("\n\n")
            if list_of_king_snakes:
                print("Average color pattern match for king snakes: %s" % (1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes)))

        updatedisplay(generationnumber)
        state.set("Done Simulating.")

    else:
        message.set("Error")


    # simulation

def game_round():
    # this makes all the animals move one square in a random direction or stay in their current square.
    for animal in list_of_coral_snakes + list_of_king_snakes + list_of_bull_frogs:
        rand = randrange(5)
        if rand == 0:
            direction = "up"
        elif rand == 1:
            direction = "down"
        elif rand == 2:
            direction = "left"
        elif rand == 3:
            direction = "right"
        else:
            direction = None
        
        if direction:
            animal.move(direction)

    # handles the conflicts in each square
    for i in range(len(array)):
        for j in range(len(array[i])):
            # only proceeds if the list isn't empty
            # print("\n\n At array[%s][%s]:" % (i, j))
            # print(array[i][j])
            if array[i][j]:
                list_of_bull_frogs_in_square = []
                list_of_coral_snakes_in_square = []
                list_of_king_snakes_in_square = []
                for animal in array[i][j]:
                    if isinstance(animal, Bull_Frog):
                        list_of_bull_frogs_in_square.append(animal)
                    elif isinstance(animal, Coral_Snake):
                        list_of_coral_snakes_in_square.append(animal)
                    elif isinstance(animal, King_Snake):
                        list_of_king_snakes_in_square.append(animal)

                # first the king snakes try to eat the coral snake
                for king_snake in list_of_king_snakes_in_square:
                    if len(list_of_coral_snakes_in_square) > 0:
                        # if this is true, the king snake tries to eat the coral snake
                        if randrange(100) in range(15):
                            if randrange(2) == 0:
                                # coral snake dies
                                list_of_coral_snakes_in_square[0].has_died()
                                del list_of_coral_snakes_in_square[0]
                            if randrange(10) not in range(7):
                                # king snake dies
                                king_snake.has_died()
                                list_of_king_snakes_in_square.remove(king_snake)
                
                # first the bull frogs eat the snakes
                # each bullfrog eats one snake. 
                # if there are no snakes in the square, each square can support up to one bullfrog.
                # if there is one bullfrog and one snake in the square, the bullfrog will eat the snake rather than the unsimulated wildlife.
                # any bullfrog that do not have food, such as three bullfrogs and one snake, will starve. In that scenario, one bullfrog starves.
                for bull_frog in list_of_bull_frogs_in_square:
                    # there's a 60% chance the bullfrog will try to eat a snake
                    if randrange(10) in range(4):
                        continue
                    if len(list_of_coral_snakes_in_square) + len(list_of_king_snakes_in_square) > 0:
                        lowest_mimicry = None
                        for snake in list_of_coral_snakes_in_square + list_of_king_snakes_in_square:
                            if lowest_mimicry is None or snake.get_mimicry() < lowest_mimicry.get_mimicry():
                                lowest_mimicry = snake
                        
                        if randrange(100) in range(110 - lowest_mimicry.get_mimicry()):
                            if isinstance(lowest_mimicry, Coral_Snake):
                                # there is a 50% chance the coral snake survives
                                if randrange(2) == 0:
                                    lowest_mimicry.has_died()
                                    list_of_coral_snakes_in_square.remove(lowest_mimicry)
                                # there is a 60% chance the bullfrog survives (based on scientific evidence). 
                                if randrange(10) in range(4):
                                    bull_frog.has_died()
                                    list_of_bull_frogs_in_square.remove(bull_frog)
                            else:
                                lowest_mimicry.has_died()
                                list_of_king_snakes_in_square.remove(lowest_mimicry)
    
    # animals that will starve instead move to an open orthogonal square. If there is no open square, they starve.
    # first starvation happens, then reproduction happens.
    for i in range(len(array)):
        for j in range(len(array[i])):
            list_of_bull_frogs_in_square = []
            list_of_coral_snakes_in_square = []
            list_of_king_snakes_in_square = []
            for animal in array[i][j]:
                if isinstance(animal, Bull_Frog):
                    list_of_bull_frogs_in_square.append(animal)
                elif isinstance(animal, Coral_Snake):
                    list_of_coral_snakes_in_square.append(animal)
                elif isinstance(animal, King_Snake):
                    list_of_king_snakes_in_square.append(animal)
            
            # checks if any orthogonal squares are empty. If so it moves the animal into one of those squares at random.
            def move_to_survive(animal):
                x = animal.get_x_position()
                y = animal.get_y_position()
                list_of_possible_directions = []
                if x >= 1 and not array[x-1][y]:
                    list_of_possible_directions.append("left")
                if x <= 18 and not array[x+1][y]:
                    list_of_possible_directions.append("right")
                if y >= 1 and not array[x][y-1]:
                    list_of_possible_directions.append("up")
                if y <= 18 and not array[x][y+1]:
                    list_of_possible_directions.append("down")
                
                if not list_of_possible_directions:
                    return None
                
                animal.move(list_of_possible_directions[randrange(len(list_of_possible_directions))])
            
            # the starving animals will move. If they cannot move (move_to_survive returns 0) then they die.

            # first the snakes move and starve.
            if len(list_of_coral_snakes_in_square) > 0 and len(list_of_king_snakes_in_square) > 0:
                coral_or_king = randrange(2)
                if coral_or_king == 0:
                    lucky_snake = list_of_coral_snakes_in_square[0]
                else:
                    lucky_snake = list_of_king_snakes_in_square[0]
            elif len(list_of_coral_snakes_in_square) > 1:
                lucky_snake = list_of_coral_snakes_in_square[0]
            elif len(list_of_king_snakes_in_square) > 1:
                lucky_snake = list_of_king_snakes_in_square[0]

            if len(list_of_king_snakes_in_square) + len(list_of_coral_snakes_in_square) > 1:
                for snake in list_of_coral_snakes_in_square + list_of_king_snakes_in_square:
                    if snake is not lucky_snake:
                        moved = move_to_survive(snake)
                        if moved is None:
                            snake.has_died()
                            if isinstance(snake, Coral_Snake):
                                list_of_coral_snakes_in_square.remove(snake)
                            else:
                                list_of_king_snakes_in_square.remove(snake)

            # now the bullfrogs move and starve.
            if len(list_of_bull_frogs_in_square) > 1:
                lucky_bullfrog = list_of_bull_frogs_in_square[0]
                for bullfrog in list_of_bull_frogs_in_square:
                    if bullfrog is not lucky_bullfrog:
                        moved = move_to_survive(bullfrog)
                        if moved is None:
                            bullfrog.has_died()
                            list_of_bull_frogs_in_square.remove(bullfrog)
    
    # now reproduction happens
    # animals are marked as having survived another round:
    for animal in list_of_bull_frogs + list_of_coral_snakes + list_of_king_snakes:
        animal.survived_another_round()

    # king snakes lay more eggs than coral snakes. In this simulation, that is being modeled as reproducing more often.
    for snake in list_of_king_snakes:
        if snake.get_rounds_survived() % 5 == 0:
            reproduced = snake.reproduce()
            if not reproduced:
                snake.change_mimicry(randrange(-2,3))
    # snakes that have survived four rounds reproduce. Check if this number makes sense. 
    # used to be all snakes, now this is just coral snakes.
    for snake in list_of_coral_snakes:
        if snake.get_rounds_survived() % 5 == 0:
            reproduced = snake.reproduce()
    
    # bullfrogs that have survived six rounds reproduce. Check if this number makes sense.
    for bullfrog in list_of_bull_frogs:
        if bullfrog.get_rounds_survived() % 8 == 0:
            bullfrog.reproduce()

    if list_of_king_snakes:
        t.color(100+int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*1.5)), 
            100-int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*1)),
            200-int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*2)))
        mimicry.set("%s\n\n%s" % (math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))), (100+int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*1.5)), 
            100-int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*1)),
            200-int(math.ceil((1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes))*2)))))
    else:
        message.set('All king snakes have died...')

def cleargrid():
    if state.get() == "Done Simulating.":
        state.set("Clearing...")
        for animal in list_of_king_snakes + list_of_coral_snakes + list_of_bull_frogs:
            animal.has_died()
        cstracer.penup()
        kstracer.penup()
        bftracer.penup()
        mimictracer.penup()
        for i in range(generations_input.get()+1):
            cstracer.undo()
            kstracer.undo()
            bftracer.undo()
            mimictracer.undo()
        cstracer.setpos(graphorigin[0],graphorigin[1])
        kstracer.setpos(graphorigin[0],graphorigin[1])
        bftracer.setpos(graphorigin[0],graphorigin[1])
        mimictracer.setpos(mimicgraphorigin[0],mimicgraphorigin[1])
        updatedisplay(0)
        t.color(100, 100, 200)
        mimicry.set("0\n\n(100, 100, 200)")
        maxgeneration.set('')
        state.set("Ready to Simulate")
        enable()
    else:
        message.set("Not Finished Simulating")

if __name__ == "__main__":
    #font = tkFont.Font()
    screen = turtle.Screen()
    screen.colormode(255)
    canvas = screen.getcanvas()
    screen.title("Simulation")
    screen.setup(1920, 1080)
    screen.bgpic('forestbackground.gif')

    state = tk.StringVar(canvas.master, 'Loading...')
    statetext = tk.StringVar(canvas.master, 'Current State:')
    message = tk.StringVar(canvas.master, 'Welcome to the simulation! \n\n Select the number of populations and generations')
    cspop = tk.StringVar(canvas.master, '0')
    kspop = tk.StringVar(canvas.master, '0')
    bfpop = tk.StringVar(canvas.master, '0')
    generation = tk.StringVar(canvas.master, '0')
    maxgeneration = tk.StringVar(canvas.master)
    mimicry = tk.StringVar (canvas.master)

    messagelabel = tk.Label (canvas.master, text = 'Console:')
    systemmessage = tk.Label (canvas.master, textvariable =message)
    statelabel = tk.Label (canvas.master, textvariable = statetext)
    simulationstate = tk.Label (canvas.master, textvariable =state, bg = 'white')
    mimicrylabel = tk.Label (canvas.master, text = 'Average Kingsnake Color')
    graphtitle = tk.Label (canvas.master, text = 'Populations of Each Species')
    yaxislabel = tk.Label (canvas.master, text = 'Qty.\n (y)')
    xaxislabel = tk.Label (canvas.master, text = 'Generations (x)')
    cspopdisplay = tk.Label (canvas.master, textvariable = cspop)
    kspopdisplay = tk.Label (canvas.master, textvariable = kspop)
    bfpopdisplay = tk.Label (canvas.master, textvariable = bfpop)
    generationdisplay = tk.Label (canvas.master, textvariable = generation)
    cspoplabel = tk.Label (canvas.master, text= '# of Coral Snakes:')
    kspoplabel = tk.Label (canvas.master, text = '# of King Snakes:')
    bfpoplabel = tk.Label (canvas.master, text= '# of Bull Frogs:')
    generationlabel = tk.Label (canvas.master, text ='Generation:')
    ygraphlabel1 = tk.Label (canvas.master, text = '350', bg = 'white')
    ygraphlabel2 = tk.Label (canvas.master, text = '0', bg = 'white')
    xgraphlabel = tk.Label (canvas.master, textvariable = maxgeneration, bg ='white')
    mimicrytext = tk.Label (canvas.master, textvariable = mimicry, bg = 'white')
    mimicrylabelnum  = tk.Label (canvas.master, text = 'Color Pattern Match \n\n (R, G, B)')
    mimicgraphlabel = tk.Label (canvas.master, text = 'Pattern Match in King Snakes (y)')
    ymimicgraphlabel1 = tk.Label (canvas.master, text = '100', bg='white')
    ymimicgraphlabel2 = tk.Label (canvas.master, text = '20', bg ='white')
    xmimicgraphlabel = tk.Label (canvas.master, textvariable = maxgeneration, bg ='white')
    mimicxaxislabel = tk.Label (canvas.master, text = 'Generations (x)')

    coralsnake_input = tk.Scale(canvas.master, from_ = 0, to = 200, orient=HORIZONTAL, length = 300, label = 'Coral Snakes')
    kingsnake_input = tk.Scale(canvas.master, from_ = 0, to = 200, orient=HORIZONTAL, length = 300, label = 'King Snakes')
    bullfrog_input = tk.Scale(canvas.master, from_= 0, to = 200, orient=HORIZONTAL, length = 300, label = 'Bull Frogs')
    generations_input = tk.Scale(canvas.master, from_= 0, to = 300, orient=HORIZONTAL, length = 300, label = 'Generations')
    spawnbutton = tk.Button(canvas.master, text='Start', command = startsimulation)
    clearbutton = tk.Button(canvas.master, text='Reset', command = cleargrid)


    makemodule(1.3, .2, messagelabel)
    makemodule(1.3, .6, systemmessage)
    makemodule(1, 1.3, simulationstate)
    makemodule(2, 1.3, statelabel)
    makemodule(1, 2, coralsnake_input)
    makemodule(1, 2.7, kingsnake_input)
    makemodule(1, 3.4, bullfrog_input)
    makemodule(1,4.1, generations_input)
    makemodule(2, 4.8, spawnbutton)
    makemodule(1, 4.8, clearbutton)
    makemodule(1, 6, mimicrytext)
    makemodule(2.5, 6, mimicrylabelnum)

    def disable():
        generations_input.config(state=DISABLED)
    def enable():
        generations_input.config(state=NORMAL)

    cspic = PhotoImage(file='coralsnake.gif').subsample(9, 9)
    kspic = PhotoImage(file='kingsnake.gif').subsample(18, 18)
    bfpic = PhotoImage(file='bullfrog.gif').subsample(9, 9)
    smallcspic = PhotoImage(file='coralsnake.gif').subsample(16, 16)
    smallkspic = PhotoImage(file='kingsnake.gif').subsample(44, 44)
    smallbfpic = PhotoImage(file='bullfrog.gif').subsample(20, 20)
    screen.addshape('coralsnake', Shape("image", cspic))
    screen.addshape('kingsnake', Shape('image', kspic))
    screen.addshape('bullfrog', Shape('image', bfpic))
    screen.addshape('minicoralsnake', Shape("image", smallcspic))
    screen.addshape('minikingsnake', Shape('image', smallkspic))
    screen.addshape('minibullfrog', Shape('image', smallbfpic))

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(10000000000000000000000000) #need to figure out how to make the setup phase not take over 30 seconds
    t.fillcolor('white')
    t.penup()
    t.goto (-halfdimension-4.3*ui_offset,-halfdimension)
    t.begin_fill()
    t.pendown()
    t.goto (-halfdimension-4.3*ui_offset,halfdimension)
    t.goto (halfdimension + 4.3*ui_offset, halfdimension)
    t.goto (halfdimension+4.3*ui_offset,-halfdimension)
    t.goto (-halfdimension-4.3*ui_offset,-halfdimension)
    t.end_fill()
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
        ypos = []
        t.setpos(-halfdimension + (.5 + a)*(boxwidth), 
                halfdimension - .5*(boxwidth))
        for b in range(rolumns):
            t.sety(halfdimension - (.5 + b)*(boxwidth))
            ypos.append(t.clone())
            gridturtles.append(t.clone())
        pos.append(ypos)

    t.setpos(graphorigin[0],graphorigin[1])
    t.pendown()
    t.fd(axislength)
    xturtle = t.clone()
    xturtle.showturtle()
    t.setpos(graphorigin[0],graphorigin[1])
    t.lt(90)
    t.fd(axislength)
    yturtle = t.clone()
    yturtle.showturtle()
    t.setpos(graphorigin[0],graphorigin[1])
    t.showturtle()
    t.penup()
    cstracer = t.clone()
    cstracer.shape('minicoralsnake')
    cstracer.pencolor('red')
    kstracer = t.clone()
    kstracer.shape('minikingsnake')
    kstracer.pencolor('black')
    bftracer = t.clone()
    bftracer.shape('minibullfrog')
    bftracer.pencolor('green')
    t.setpos(mimicgraphorigin[0],mimicgraphorigin[1])
    t.pendown()
    t.fd(axislength)
    xturtle2 = t.clone()
    xturtle2.showturtle()
    t.setpos(mimicgraphorigin[0],mimicgraphorigin[1])
    t.rt(90)
    t.fd(axislength)
    yturtle2 = t.clone()
    yturtle2.showturtle()
    t.setpos(mimicgraphorigin[0],mimicgraphorigin[1])
    t.showturtle()
    t.penup()
    mimictracer = t.clone()
    mimictracer.shape('minikingsnake')
    mimictracer.pencolor(100, 100, 200)

    makemodule(-13.5, .25, graphtitle)
    makemodule(-11.6, .25, yaxislabel)
    makemodule(-13.3, 4.3, xaxislabel)
    makemodule(-13, 4.6, cspopdisplay)
    makemodule(-12, 4.6, cspoplabel)
    makemodule(-13, 4.9, kspopdisplay)
    makemodule(-12, 4.9, kspoplabel)
    makemodule(-13, 5.2, bfpopdisplay)
    makemodule(-12, 5.2, bfpoplabel)
    makemodule(-13, 5.5, generationdisplay)
    makemodule(-12, 5.5, generationlabel)
    makemodule(-11.3, .6, ygraphlabel1)
    makemodule(-11.3, 4, ygraphlabel2)
    makemodule(-15, 4.2, xgraphlabel)
    makemodule(-13.3, 5.8, mimicgraphlabel)
    makemodule(-11.3, 6, ymimicgraphlabel1)
    makemodule(-11.3, 9.4, ymimicgraphlabel2)
    makemodule(-15, 9.7, xmimicgraphlabel)
    makemodule(-13.3, 9.7, mimicxaxislabel)

    t.setpos(-halfdimension - 3.5*ui_offset, -halfdimension+2*ui_offset)
    kingsnakemodel = t.clone()
    kingsnakemodel.shape('kingsnake')
    t.setpos(-halfdimension - 2.3*ui_offset, -halfdimension+2.5*ui_offset)
    t.shape('circle')
    t.color(100, 100, 200)
    mimicry.set('0 \n\n 100, 200, 200')
    t.shapesize(10,10,1)
    makemodule(1.3, 5.5, mimicrylabel)

    state.set('Ready to Simulate')


# this creates a 3d array. The 2d base of the array has a width and height of the
# var values width and height, and the vertical arrays have limitless length.
# this is because when multiple animals move into one square, they will be stacked
# vertically in that array. Therefore it is limitless.

# sets up classes. The turtle class has an x position and a y position,
# and four move commands.
class Turtle:

    def __init__(self, x_position, y_position, rounds_survived=0):
        print("x and y position: %s %s" % (x_position, y_position))
        self.x = x_position
        self.y = y_position
        self.object = pos[x_position][y_position].clone()
        self.object.showturtle()
        if self.__class__.__name__ == "Coral_Snake":
            self.object.shape('coralsnake')
            #self.object.color('red')
        if self.__class__.__name__ == "Bull_Frog":
            self.object.shape('bullfrog')
            #self.object.color('orange')
        array[x_position][y_position].append(self)
        
        self.rounds_survived = rounds_survived
            

    def get_x_position(self):
        return self.x
    
    def get_y_position(self):
        return self.y
    
    def get_rounds_survived(self):
        return self.rounds_survived

    def get_object(self):
        return self.object
    
    def survived_another_round(self):
        self.rounds_survived += 1

    def move(self, direction):
        width = get_width()
        height = get_height()
        object = self.object

        x = self.x
        y = self.y
        array[x][y].remove(self)
        if direction == "up":
            if y >= 1:
                y -= 1
                object.seth(90)
                object.fd(boxwidth)
        elif direction == "down":
            if y <= height - 4:
                height += 1
                object.seth(270)
                object.fd(boxwidth)
        elif direction == "left":
            if x >= 1:
                x -= 1
                object.seth(180)
                object.fd(boxwidth)
        elif direction == "right":
            if x <= width - 2:
                x += 1
                object.seth(0)
                object.fd(boxwidth)
        else:
            return "error"
        
        # debugging
        #print("Move from %s %s to %s %s" % (self.x, self.y, x, y))

        # changes the x and y values of the animal
        self.x = x
        self.y = y

        array[x][y].append(self)

    # it checks all 8 slots around this animal's position. If one is empty, it creates a new animal in that slot. When the coral snakes reproduce, their mimicry changes a bit
    def reproduce(self):
        x = self.x
        y = self.y
        reproduced = False
        for i in range(3):
            if reproduced:
                break
            if (x + (i-1)) in range(width):
                for j in range(3):
                    if reproduced:
                        break
                    if (y + (j-1)) in range(height):
                        # checks if the list is empty
                        if not array[x + (i-1)][y + (j-1)]:
                            if self.__class__.__name__ == "Coral_Snake":
                                # need to make it so that coral snakes take both their parents' mimicries and then average it as their own mimicry.
                                list_of_coral_snakes.append(
                                    Coral_Snake((x + i - 1), (y + j - 1))
                                    )
                            elif self.__class__.__name__ == "King_Snake":
                                list_of_king_snakes.append(King_Snake((x + i - 1), (y + j - 1), mimicry=self.get_mimicry()))
                            elif self.__class__.__name__ == "Bull_Frog":
                                list_of_bull_frogs.append(Bull_Frog((x + i - 1), (y + j - 1)))

                            # sets reproduced to true so that the rest of the loops break and the animal doesn't reproduce twice
                            reproduced = True
                            break
    
    def has_died(self):
        print("I'm at %s %s" % (self.x, self.y))
        array[self.x][self.y].remove(self)
        object = self.object
        object.shape('square')
        object.color('red')
        self.object.shapesize(2.5, 2.5, 1)
        object.hideturtle()
        del object

class Coral_Snake(Turtle):
    def __init__(self, x_position, y_position, rounds_survived=0):
        super().__init__(x_position, y_position, rounds_survived)
        self.mimicry = 100
    
    def has_died(self):
        super().has_died()
        list_of_coral_snakes.remove(self)

    def get_mimicry(self):
        return self.mimicry

class King_Snake(Turtle):
    def __init__(self, x_position, y_position, mimicry=None, rounds_survived=0):
        super().__init__(x_position, y_position, rounds_survived)
        if mimicry is None:
            self.mimicry = 0  # randrange(0,100,10) commented out because king snakes aren't given mimicry during setup an they should have 0 mimicry.
        else:
            self.mimicry = mimicry
            # print("parent mimicry: %s" % mimicry)
            self.change_mimicry(randrange(-2,3))  # -2,3
            # print("child mimicry: %s" % self.mimicry)

        #self.object.shape('kingsnake')
        self.object.shape('circle')
        self.object.shapesize(1.8, 1.8, 1)
        self.object.color((100+int(self.get_mimicry()*1.5), 100-int(self.get_mimicry()*1), 200-int(self.get_mimicry()*2)))


    def get_mimicry(self):
        return self.mimicry

    def change_mimicry(self, increment):
        self.mimicry += (increment * 10)
        if self.mimicry < 0:
            self.mimicry = 0
        elif self.mimicry > 100:
            self.mimicry = 100
    
    def has_died(self):
        super().has_died()
        list_of_king_snakes.remove(self)
        

class Bull_Frog(Turtle):
    def has_died(self):
        super().has_died()
        list_of_bull_frogs.remove(self)
    
    def eats(snake):
        if randrange(100) in range(110 - snake.mimicry):
            snake.has_died()

# main function. 
def main():
    #print(array)

    #current number of rounds. In the simulation it will be infinite? Or will the user set how many rounds?

    turtle.done()

main()

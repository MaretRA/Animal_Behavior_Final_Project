from random import randrange


# sets up width, height, and array
width = 20
height = 20


def get_width():
    return width

def get_height():
    return height



# this creates a 3d array. The 2d base of the array has a width and height of the
# var values width and height, and the vertical arrays have limitless length.
# this is because when multiple animals move into one square, they will be stacked
# vertically in that array. Therefore it is limitless.
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

# sets up classes. The turtle class has an x position and a y position,
# and four move commands.
class Turtle:

    def __init__(self, x_position, y_position, rounds_survived=0):
        print("x and y position: %s %s" % (x_position, y_position))
        self.x = x_position
        self.y = y_position
        array[x_position][y_position].append(self)
        
        self.rounds_survived = rounds_survived
            

    def get_x_position(self):
        return self.x
    
    def get_y_position(self):
        return self.y
    
    def get_rounds_survived(self):
        return self.rounds_survived
    
    def survived_another_round(self):
        self.rounds_survived += 1

    def move(self, direction):
        width = get_width()
        height = get_height()

        x = self.x
        y = self.y
        array[x][y].remove(self)
        if direction == "up":
            if y >= 1:
                y -= 1
        elif direction == "down":
            if y <= height - 2:
                height += 1
        elif direction == "left":
            if x >= 1:
                x -= 1
        elif direction == "right":
            if x <= width - 2:
                x += 1
        else:
            return "error"
        
        # debugging
        print("Move from %s %s to %s %s" % (self.x, self.y, x, y))

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
        if not mimicry:
            self.mimicry = 0  # randrange(0,100,10) commented out because king snakes aren't given mimicry during setup an they should have 0 mimicry.
        else:
            self.mimicry = mimicry
            self.change_mimicry(randrange(-1,2))
    
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

# setup. Creates all the snakes and bullfrogs.
def setup(num_coral_snakes, num_king_snakes, num_bullfrogs):
    # creates an array of all possible starting locations
    possible_starting_locations = []
    for i in range(20):
        for j in range(20):
            possible_starting_locations.append([i,j])
    
    if num_coral_snakes + num_king_snakes + num_bullfrogs > len(possible_starting_locations):
        return "Error, more animals than starting locations."
    
    # adds the coral_snakes
    for cs in range(num_coral_snakes):
        ind = randrange(len(possible_starting_locations))
        indices = possible_starting_locations[ind]
        # prints indices for debugging purposes.
        print("indices[0] = %s, indices[1] = %s" % (indices[0], indices[1]))
        list_of_coral_snakes.append(Coral_Snake(indices[0], indices[1], randrange(4)))
        del possible_starting_locations[ind]
    
    # adds the king snakes
    for ks in range(num_king_snakes):
        ind = randrange(len(possible_starting_locations))
        indices = possible_starting_locations[ind]
        list_of_king_snakes.append(King_Snake(indices[0], indices[1], randrange(4)))
        del possible_starting_locations[ind]

    # adds the bullfrogs
    for bf in range(num_bullfrogs):
        ind =randrange(len(possible_starting_locations))
        indices = possible_starting_locations[ind]
        list_of_bull_frogs.append(Bull_Frog(indices[0], indices[1], randrange(4)))
        del possible_starting_locations[ind]
        



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
            print("\n\n At array[%s][%s]:" % (i, j))
            print(array[i][j])
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
                
                # first the bull frogs eat the snakes
                # each bullfrog eats one snake. 
                # if there are no snakes in the square, each square can support up to one bullfrog.
                # if there is one bullfrog and one snake in the square, the bullfrog will eat the snake rather than the unsimulated wildlife.
                # any bullfrog that do not have food, such as three bullfrogs and one snake, will starve. In that scenario, one bullfrog starves.
                for bull_frog in list_of_bull_frogs_in_square:
                    if len(list_of_coral_snakes_in_square) + len(list_of_king_snakes_in_square) > 0:
                        lowest_mimicry = None
                        for snake in list_of_coral_snakes_in_square + list_of_king_snakes_in_square:
                            if not lowest_mimicry or snake.get_mimicry() < lowest_mimicry.get_mimicry():
                                lowest_mimicry = snake
                        
                        if randrange(100) in range(100 - lowest_mimicry.get_mimicry()):
                            if isinstance(lowest_mimicry, Coral_Snake):
                                # there is a 50% chance the coral snake survives
                                if randrange(2) == 0:
                                    lowest_mimicry.has_died()
                                    list_of_coral_snakes_in_square.remove(lowest_mimicry)
                                # there is a 60% chance the bullfrog survives (based on scientific evidence). 
                                if randrange(10) in range(4):
                                    bull_frog.has_died()
                                    list_of_bull_frogs_in_square.remove(bull_frog)
                                list_of_coral_snakes_in_square.remove(lowest_mimicry)
                            else:
                                lowest_mimicry.has_died()
                                list_of_king_snakes_in_square.remove(lowest_mimicry)
                
                # animals are marked as having survived another round:
                for animal in array[i][j]:
                    animal.survived_another_round()
                
                # snakes that have survived three rounds reproduce. Check if this number makes sense. 
                for snake in list_of_coral_snakes_in_square + list_of_king_snakes_in_square:
                    if snake.get_rounds_survived() % 4 == 0:
                        snake.reproduce()
                
                # bullfrogs that have survived five rounds reproduce. Check if this number makes sense.
                for bullfrog in list_of_bull_frogs_in_square:
                    if bullfrog.get_rounds_survived() % 6 == 0:
                        bullfrog.reproduce()
                
                # animals no longer starve

                # # if there is more than one snake in a square, further snakes will starve
                # first = True
                # for snake in list_of_coral_snakes_in_square + list_of_king_snakes_in_square:
                #     if not first:
                #         snake.has_died()
                #         if isinstance(snake, Coral_Snake):
                #             list_of_coral_snakes_in_square.remove(snake)
                #         else:
                #             list_of_king_snakes_in_square.remove(snake)
                #     else:
                #         first = False
                
                # # if there are more than two bullfrogs in a square, the bullfrog will starve. This may be subject to change later.
                # # the previous idea I had for this scenario was to have the extra bullfrogs move to adjacent squares, but 
                # # since the simulation occurs one square at a time that would lead to the bullfrog being used again in that square.
                # # the other way to do this is to wait for this double for loop to end and then run another one just to have the bullfrogs move.
                # # but for now let's just starve them. This also deals with the potential overpopulation issues. And if we have bullfrogs move,
                # # then snakes should move too. Which can of course be done in the same way.
                # first = True
                # for bullfrog in list_of_bull_frogs_in_square:
                #     if not first:
                #         bullfrog.has_died()
                #         list_of_bull_frogs_in_square.remove(bullfrog)
                #     else:
                #         first = False


# the final thing that needs to be added in (besides the code that needs to be written to replace the comments) is the ui.
# each square will support only two animals: up to one snake and one bullfrog. When the animals move it will be shown on the ui, and 
# then after all the movements have been made, animals will die and reproduce. There should also be sliders, to set the starting
# numbers of coral snakes, king snakes, and bull frogs, and there should be counters to show the current number of each. 
# and maybe also counters to show the percentage of king snakes that have each percentage of matching pattern.

# lastly, for the matching pattern for king snakes, I propose we represent this by making coral snakes a vibrant red, and king
# snakes a vibrant blue, and over time they become more red. 


# main function. 
def main():
    setup(40, 40, 40)
    print(array)

    # current number of rounds. In the simulation it will be infinite? Or will the user set how many rounds?
    for i in range(20):
        game_round()
        print("Number of coral snakes: %s" % len(list_of_coral_snakes))
        print("Number of king snakes: %s" % len(list_of_king_snakes))
        print("Number of bullfrogs: %s" % len(list_of_bull_frogs))
        print("\n\n")
        print("Average color pattern match for king snakes: %s" % (1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes)))

main()

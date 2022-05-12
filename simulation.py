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
        # print("x and y position: %s %s" % (x_position, y_position))
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
        # print("Move from %s %s to %s %s" % (self.x, self.y, x, y))

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
        
        return reproduced
    
    def has_died(self):
        # print("I'm at %s %s" % (self.x, self.y))
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
        if mimicry is None:
            self.mimicry = 0  # randrange(0,100,10) commented out because king snakes aren't given mimicry during setup an they should have 0 mimicry.
        else:
            self.mimicry = mimicry
            # print("parent mimicry: %s" % mimicry)
            self.change_mimicry(randrange(-2,3))  # -2,3
            # print("child mimicry: %s" % self.mimicry)
    
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
        # print("indices[0] = %s, indices[1] = %s" % (indices[0], indices[1]))
        list_of_coral_snakes.append(Coral_Snake(indices[0], indices[1], rounds_survived=randrange(4)))
        del possible_starting_locations[ind]
    
    # adds the king snakes
    for ks in range(num_king_snakes):
        ind = randrange(len(possible_starting_locations))
        indices = possible_starting_locations[ind]
        list_of_king_snakes.append(King_Snake(indices[0], indices[1], rounds_survived=randrange(4)))
        del possible_starting_locations[ind]

    # adds the bullfrogs
    for bf in range(num_bullfrogs):
        ind =randrange(len(possible_starting_locations))
        indices = possible_starting_locations[ind]
        list_of_bull_frogs.append(Bull_Frog(indices[0], indices[1], rounds_survived=randrange(4)))
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


# main function. 
def main():
    setup(120, 120, 100)

    # current number of rounds. In the simulation it will be infinite? Or will the user set how many rounds?
    for i in range(200):
        game_round()
        print("Game round: %s" % str(i+1))
        print("Number of coral snakes: %s" % len(list_of_coral_snakes))
        print("Number of king snakes: %s" % len(list_of_king_snakes))
        print("Number of bullfrogs: %s" % len(list_of_bull_frogs))
        # print("\n\n")
        print("Average color pattern match for king snakes: %s" % (1.0 * sum([snake.get_mimicry() for snake in list_of_king_snakes])/len(list_of_king_snakes)) if len(list_of_king_snakes) > 0 else "They are all dead.")
        if not list_of_king_snakes:
            print("All King Snakes are dead.")
            break

    print([snake.get_mimicry() for snake in list_of_king_snakes])
    # for king_snake in list_of_king_snakes:
        # print("x y coords: %s %s" % (king_snake.get_x_position(), king_snake.get_y_position()))
        # print("at that square:")
        # print(array[king_snake.get_x_position()][king_snake.get_y_position()])

main()

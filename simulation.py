from random import randrange

# sets up width, height, and array
width = 20
height = 20

# this creates a 3d array. The 2d base of the array has a width and height of the
# var values width and height, and the vertical arrays have limitless length.
# this is because when multiple animals move into one square, they will be stacked
# vertically in that array. Therefore it is limitless.
array = [[[]] * height] * width


# creates lists of all animals
list_of_coral_snakes = []
list_of_king_snakes = []
list_of_bull_frogs = []

# sets up classes. The turtle class has an x position and a y position,
# and four move commands.
class Turtle:

    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position
        array[x_position][y_position].append(self)
        
        self.rounds_survived = 0
            

    def get_x_position(self):
        return self.x
    
    def get_y_position(self):
        return self.y
    
    def get_rounds_survived(self):
        return self.rounds_survived
    
    def survived_another_round(self):
        self.rounds_survived += 1

    def move(self, direction):
        x = self.x
        y = self.y
        array[x][y].remove(self)
        if direction == "up":
            if y >= 1:
                y -= 1
        elif direction == "down":
            if y <= height:
                height += 1
        elif direction == "left":
            if x >= 1:
                x += 1
        elif direction == "right":
            if x <= width:
                x -= 1
        else:
            return "error"

        array[x][y].append(self)

    # it checks all 8 slots around this animal's position. If one is empty, it creates a new animal in that slot. When the coral snakes reproduce, their mimicry changes a bit
    def reproduce(self, other_animal=None):
        x = self.x
        y = self.y
        reproduced = False
        for i in range(3):
            if reproduced:
                break
            if (x + (i-1) - 1) in range(width):
                for j in range(3):
                    if reproduced:
                        break
                    if (y + (j-1) - 1) in range(height):
                        # checks if the list is empty
                        if not array[width][height]:
                            if self.__class__.__name__ == "Coral_Snake":
                                # need to make it so that coral snakes take both their parents' mimicries and then average it as their own mimicry.
                                list_of_coral_snakes.append(
                                    Coral_Snake(
                                        (x + i - 2), (y + j - 2), 
                                        mimicry=((self.get_mimicry() + other_animal.get_mimicry())/2)
                                        )
                                    )
                            elif self.__class__.__name__ == "King_Snake":
                                list_of_king_snakes.append(King_Snake((x + i - 2), (y + j - 2)))
                            elif self.__class__.__name__ == "Bull_Frog":
                                list_of_bull_frogs.append(Bull_Frog((x + i - 2), (y + j - 2)))

                            # sets reproduced to true so that the rest of the loops break and the animal doesn't reproduce twice
                            reproduced = True
                            break
    
    def has_died(self):
        array[self.x][self.y].remove(self)

class Coral_Snake(Turtle):
    def __init__(self, x_position, y_position, mimicry=None):
        super().__init__(x_position, y_position)
        if not mimicry:
            self.mimicry = randrange(0,100,10)
        else:
            self.mimicry = mimicry
            self.change_mimicry(randrange(-1,1))
        
    
    def get_mimicry(self):
        return self.mimicry

    def change_mimicry(self, increment):
        self.mimicry += (increment * 10)
    
    def has_died(self):
        super().has_died(self)
        list_of_coral_snakes.remove(self)

class King_Snake(Turtle):
    def __init__(self, x_position, y_position):
        super().__init__(x_position, y_position)
        self.mimicry = 100
    
    def has_died(self):
        super().has_died(self)
        list_of_king_snakes.remove(self)
        

class Bull_Frog(Turtle):
    def has_died(self):
        super().has_died(self)
        list_of_bull_frogs.remove(self)
    
    def eats(snake):
        if randrange(100) in range(110-snake.mimicry):
            snake.has_died()

# setup

# need to code this

# simulation

# this makes all the animals move one square in a random direction or stay in their current square.
for animal in list_of_coral_snakes + list_of_king_snakes + list_of_bull_frogs:
    rand = randrange(5)
    if rand == 1:
        direction = "up"
    elif rand == 2:
        direction = "down"
    elif rand == 3:
        direction = "left"
    elif rand == 4:
        direction = "right"
    else:
        direction = None
    
    if direction:
        animal.move(direction)

# handles the conflicts in each square
for i in array:
    for j in array[i]:
        # only proceeds if the list isn't empty
        if array[i][j]:
            list_of_bull_frogs_in_square = []
            list_of_coral_snakes_in_square = []
            list_of_king_snakes_in_square = []
            for animal in array[i][j]:
                if isinstance(animal, Bull_Frog):
                    list_of_bull_frogs_in_square.append(animal)
                elif isinstance(animal, Bull_Frog):
                    list_of_bull_frogs_in_square.append(animal)
                elif isinstance(animal, Bull_Frog):
                    list_of_bull_frogs_in_square.append(animal)
            
            # first the bull frogs eat the snakes
            # each bullfrog eats one snake. 
            # if there are no snakes in the square, each square can support up to one bullfrog.
            # if there is one bullfrog and one snake in the square, the bullfrog will eat the snake rather than the unsimulated wildlife.
            # any bullfrog that do not have food, such as three bullfrogs and one snake, will starve. In that scenario, one bullfrog starves.

            # eating code

            # bullfrog starving code

            # each square can support only one snake population. If there are two snakes, one will starve.

            # snake starving code

            # now snakes and bullfrogs that survived the round will reproduce.

            # animals reproducing code. 

            # each square can only visually support one bullfrog and one snake. Therefore, if there are two or more bullfrogs in
            # one square at the end of the round, the second bullfrog must move to a nearby square. If none are available
            # (which would be extraordinarily rare), the bullfrog dies.

            # extra bullfrog moving code.

# the final thing that needs to be added in (besides the code that needs to be written to replace the comments) is the ui.
# each square will support only two animals: up to one snake and one bullfrog. When the animals move it will be shown on the ui, and 
# then after all the movements have been made, animals will die and reproduce. There should also be sliders, to set the starting
# numbers of coral snakes, king snakes, and bull frogs, and there should be counters to show the current number of each. 
# and maybe also counters to show the percentage of king snakes that have each percentage of matching pattern.

# lastly, for the matching pattern for king snakes, I propose we represent this by making coral snakes a vibrant red, and king
# snakes a vibrant blue, and over time they become more red. 






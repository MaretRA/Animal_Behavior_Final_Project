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
        array[x_postion][y_position].append(self)
    
    def move_up():
        if y >= 1:
            y -= 1

    def move_down():
        if y <= height:
            height += 1

    def move_left():
        if x >= 1:
            x += 1

    def move_right():
        if x <= width:
            x -= 1

    # it checks all 8 slots around this animal's position. If one is empty, it creates a new animal in that slot. When the coral snakes reproduce, their mimicry changes a bit
    def reproduce(self):
        reproduced = False
        for i in range(3):
            if (x + (i-1) - 1) in range(width):
                for j in range(3):
                    if (y + (i-1) - 1) in range(height):
                        if not array[width][height]:
                            if self.__class__.__name__ == "Coral_Snake":
                                # need to make it so that coral snakes take both their parents' mimicries and then average it as their own mimicry.
                                list_of_coral_snakes.append(Coral_Snake((x + i - 2), (y + j - 2)))
                            elif self.__class__.__name__ == "King_Snake":
                                list_of_king_snakes.append(King_Snake((x + i - 2), (y + j - 2)))
                            elif self.__class__.__name__ == "Bull_Frog":
                                list_of_bull_frogs.append(Bull_Frog((x + i - 2), (y + j - 2)))

                            # sets reproduced to true so that the rest of the loops break and the animal doesn't reproduce twice
                            reproduced = True
                            break
                if reproduced:
                    break

class Coral_Snake(Turtle):
    # I need to check how replacing/extending parent functions works.
    def __init__(self, x_position, y_position, mimicry=None):
        self.x = x_position
        self.y = y_position
        array[x_postion][y_position].append(self)
        if not mimicry:
            self.mimicry = randrange(0,100,10)
        else:
            self.mimicry = mimicry
            change_mimicry(randrange(-1,1))
        

    def change_mimicry(increment):
        self.mimicry += (increment * 10)

class King_Snake(Turtle):
    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position
        self.mimicry = 100

class Bull_Frog(Turtle):
    None

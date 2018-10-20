from colors import Color_Palette
import pygame
import random

colors = Color_Palette()

CELL_SIZE = 40
GRID_SIZE_X = 20
GRID_SIZE_Y = 30

#Display dimensions
display_height = GRID_SIZE_X*CELL_SIZE
display_width = GRID_SIZE_Y*CELL_SIZE

class Agent():
    def __init__(self, brain):
        pass
        # if(isinstance(brain, nn.NeuralNetwork)):
        #     self.brain = brain.copy()
        #     self.brain.mutate(mutation)
        # else:
        #     self.brain = nn.NeuralNetwork(5,8,2)
        # self.score = 0
        # self.fitness = 0

    def think(self,wall):
        pass

class Snake(Agent):
    def __init__(self, x, y, brain,size,speed =1, length=20, dir =(-1,0)):
        self.parts = [Snakepart(x+i*size, y, size) for i in range(length)]
        self.size = size
        Agent.__init__(self,brain)
        self.dir = dir
        self.speed = speed


    def draw(self, display):
        for part in self.parts:
            part.draw(display)

    def update(self,gameDisplay, draw = False):
        pass

    def copy(self):
        return Snake(x,y,self.brain)

    def tail_coords(self):
        return self.parts[len(self.parts)-1].x,self.parts[len(self.parts)-1].y

    def head_x(self):
        return self.parts[0].x
    def head_y(self):
        return self.parts[0].y

    def all_coords(self):
        return [(part.x,part.y) for part in self.parts]


    def move(self):
        for i in range(len(self.parts)-1,0,-1):
            self.parts[i].x = self.parts[i-1].x
            self.parts[i].y = self.parts[i-1].y
        self.parts[0].x = (self.parts[0].x + self.dir[0]*self.size) % display_width
        self.parts[0].y = (self.parts[0].y + self.dir[1]*self.size) % display_height

    def add_part(self, color):
        tail = self.tail_coords()
        self.parts.append(Snakepart(tail[0],tail[1],self.size, color=color))

    def eat_pickup(self, color):
        self.add_part(color)


class Snakepart():
    def __init__(self,x,y, size, color = None):
        self.x = x
        self.y = y
        self.size = size
        if color:
            self.color = color
        else:
            self.color = colors.random_color()

    def draw(self, display):
        pygame.draw.rect(display, self.color, [self.x, self.y, self.size-2, self.size-2])


class Pickup():
    def __init__(self, snake,size, value = 1, color = None,coords = None):
        if not coords:
            coords = random_cords(snake)
        self.x = coords[0]
        self.y = coords[1]
        self.value = value
        self.size = size
        if color:
            self.color = color
        else:
            self.color = colors.random_color()

    def draw(self,display):
        pygame.draw.rect(display, self.color, [self.x, self.y, self.size-5, self.size-5])

def random_cords(snake):
    while True:
        cords = (random.randrange(GRID_SIZE_X-1)*CELL_SIZE,random.randrange(GRID_SIZE_Y-1)*CELL_SIZE)
        if cords not in snake.all_coords() and cords[0] < display_width and cords[1] < display_height:
            return cords

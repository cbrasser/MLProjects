import random
import numpy as np
import neuralNetwork as nn
import pygame
import math

#--------------------Colors-----------------------
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)

#---------------------sizes--------------------

display_width = 1600
display_height = 1200
wall_width= display_width/50
wall_height=display_height/6
x =  (display_width * 0.2)
y = (display_height * 0.5)

def mutation(x):
	if random.randrange(0,1)<0.1:
		offset = np.random.normal()*0.5
		newx = x + offset
		return newx
	else:
		return x

class Copter():
	def __init__(self, x, y, brain,speed =0,velocity =0, gravity=1, acceleration = 2):
		self.x = x
		self.y = y
		self.speed = speed
		self.gravity = gravity 
		self.acceleration = acceleration
		self.velocity = velocity
		self.copterImg = pygame.image.load('copter.png')
		if(isinstance(brain, nn.NeuralNetwork)):
			self.brain = brain.copy()
			self.brain.mutate(mutation)
		else:
			self.brain = nn.NeuralNetwork(5,8,2)
		self.score = 0
		self.fitness = 0



	def draw(self, gameDisplay):
		gameDisplay.blit(self.copterImg, (self.x,self.y))
		#pygame.draw.rect(gameDisplay, white, [self.x, self.y, 20, 20])


	def update(self,gameDisplay, draw = False):
		self.score+=1
		self.velocity +=self.gravity
		self.y +=self.velocity
		# if draw:
		# 	self.draw(gameDisplay)

	def copy(self):
		return Copter(x,y,self.brain)

	def forward(self):
		self.x += self.speed

	def up(self):
		self.y += self.gravity

	def down(self):
		self.y -= gravity

	def think(self,wall):
		check_wall_up = wall.upper_walls[40]
		check_wall_down = wall.lower_walls[40]

		inputs = []
		inputs.append(check_wall_down.x)
		inputs.append(check_wall_up.y)
		inputs.append(check_wall_down.y)
		inputs.append(self.y)
		inputs.append(self.velocity)

		action = self.brain.predict(inputs)

		if action[1] > action[0]:
			self.velocity -= self.acceleration

class Wall_element:

	def __init__(self, x,y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color

	def draw(self,gameDisplay, xmod =0, ymod =0, wmod =0, hmod =0):
		if self.color==green:
			#pygame.draw.rect(gameDisplay, black, [self.x, 0, self.width, ],1)
			pygame.draw.rect(gameDisplay, self.color, [self.x, 0, self.width, self.y+self.height])
		else:
			#	pygame.draw.rect(gameDisplay, black, [self.x, self.y, self.width, self.height],1)
			pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, display_height-self.y])
    
class Wall():
	def __init__(self):
		self.prev_height_top = 0
		self.prev_x = -5
		self.prev_height_bottom = display_height-wall_height
		self.upper_walls = []
		self.lower_walls = []
		self.direction = [0,0]

		for i in range(0,55):
			self.upper_walls.append(Wall_element(-wall_width+i*wall_width,0,wall_width,wall_height, green))
			self.lower_walls.append(Wall_element(-wall_width+i*wall_width,self.prev_height_bottom,wall_width,wall_height,blue))

	def update_wallgroup(self,gameDisplay,walls, draw):
		global direction
		for index in range(0,len(walls)):
			if index < len(walls)-1:
				walls[index].y = walls[index+1].y
			else:
				if self.direction[0]==1:
					walls[index].y= walls[index].y - (self.direction[1]+1)*2
					if (walls[index].color==green and walls[index].y<-150):
						self.direction = [0,0]
					self.direction[1]+=1
				else:
					walls[index].y= walls[index].y + (self.direction[1]+1)*2
					if (walls[index].color==blue and walls[index].y>display_height-20):
						self.direction = [1,0]
					self.direction[1]+=1
			if draw:
				walls[index].draw(gameDisplay)
			# if copter_x>=walls[index].x and copter_x <= (walls[index].x+walls[index].width):
			# 	if copter_y >= walls[index].y and copter_y <= (walls[index].y+walls[index].height):
			# 		return True
		return False;


	def update(self,gameDisplay,drawing=True):
		#Only update the lower walls if the upper walls did not lead to a crash
		next_direction = random.randrange(0,10)
		if next_direction <= self.direction[1]:
			self.direction = [math.floor((self.direction[0]+1)/2),0]
		self.update_wallgroup(gameDisplay, self.upper_walls, drawing)
		self.update_wallgroup(gameDisplay,self.lower_walls, drawing)		

	def draw(self,gameDisplay):
		for wall in self.upper_walls:
			wall.draw(gameDisplay)
		for wall in self.lower_walls:
			wall.draw(gameDisplay)

	def crashCheck(self, copter_x,copter_y):
		for wall in self.upper_walls:
			if copter_x>=wall.x and copter_x <= (wall.x+wall.width):
				if copter_y<=wall.y+wall.height:
					return True
		for l_wall in self.lower_walls:
			if copter_x>=l_wall.x and copter_x <= (l_wall.x+l_wall.width):
				if copter_y >= l_wall.y:
					return True
		return False

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)


def crash():
    message_display('You Crashed')

def display_score(score, gameDisplay):

    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(score), True, black)
    gameDisplay.blit(text,(20,200))

def random_action2():
    return random.randrange(0,2)





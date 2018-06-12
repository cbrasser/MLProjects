import pygame
import numpy as np
import random
import perfect_player
import neuralNetwork as nn

display_width = 1250
display_height = 750

#---------------------colors--------------------
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
random_color = (200, 120, 4)

#----------------------Variables----------------

ball_radius = 20
bar_width= 70
bar_height = 10

def mutation(x):
	if random.randrange(0,1)<0.1:
		offset = np.random.normal()*0.5
		newx = x + offset
		return newx
	else:
		return x

class Player:
	def __init__(self, position,width, height, color,brain,display_w = display_width, display_h=display_height, movespeed = 20):
		self.score = 0
		self.direction = 0
		self.width = width
		self.height = height
		self.color = color
		self.position = position
		self.movespeed = movespeed
		self.x = display_w/2 - self.width/2
		#top
		if position == 0:
			self.y = 0
		else:
			self.y = display_h - self.height
		if(isinstance(brain, nn.NeuralNetwork)):
			self.brain = brain.copy()
			self.brain.mutate(mutation)
		else:
			#4 inputs, 8 hidden, 3 output. might change that
			self.brain = nn.NeuralNetwork(2,8,3)

	def draw(self, gameDisplay):
		pygame.draw.rect(gameDisplay, self.color, [self.x,self.y,self.width,self.height])

	def update(self, gameDisplay, draw=True):
		self.score +=1
		self.x += self.direction*self.movespeed
		if self.x <= 0:
			self.x = 0
		elif self.x + self.width >= display_width:
			self.x = display_width-self.width
		if draw:
			self.draw(gameDisplay)

	def copy(self):
		return Player(self.position, self.width, self.height, self.color, self.brain, movespeed =self.movespeed)

	def think(self, ball):
		inputs = []
		inputs.append(ball.x)
		#inputs.append(ball.y)
		inputs.append(self.x + self.width/2)
		#inputs.append(self.y)
		#inputs.append(ball.direction)

		action = self.brain.predict(inputs)

		if action[1] > action[0]:
			if action[1] > action[2]:
				self.direction = 1
			else:
				self.direction = 0
		elif action[0]>action[2]:
			self.direction = -1
		else:
			direction = 0

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Ball:
	def __init__(self, radius, max_speed,initial_speed, acceleration_per_bounce, color = (255,0,0,)):
		self.max_speed = max_speed
		self.initial_speed = initial_speed
		self.acceleration_per_bounce = acceleration_per_bounce
		self.velocity = initial_speed
		self.direction =  float(np.pi*3/4) -float(random.randrange(90))/180*np.pi
		self.color = color
		self.radius = radius
		self.x = display_width/2-self.radius/2
		self.y = display_height/2-self.radius/2

	def draw(self, gameDisplay):
		pygame.draw.circle(gameDisplay, self.color,(int(self.x),int(self.y)),self.radius)

	def hit_player(self):
		self.velocity = clamp(self.velocity+self.acceleration_per_bounce, self.initial_speed, self.max_speed)
		self.direction = 2*np.pi - self.direction
		if random.randrange(100)>=80:
			if random.randrange(100)>= 50:
				self.direction += float(random.randrange(30)/180*np.pi)
			else:
				self.direction -= float(random.randrange(30)/180*np.pi)

	def hit_sidewalls(self):
		self.direction = np.pi - self.direction

	def check_player_collision(self,player):
		if self.x >= player.x  and self.x <= player.x + player.width:
			if self.y >= player.y and self.y <= player.y + player.height:
				print "hit"
				return True
		return False

	def reached_player_position(self):
		if self.y <= bar_height or self.y >= display_height - bar_height:
			return True
		else:
			return False

	def update(self, gameDisplay, draw=True):
		self.x += np.cos(self.direction)*self.velocity
		self.y += np.sin(self.direction)*self.velocity
		#Collisions with side walls
		if self.x <= 0 or self.x >= display_width:
			self.x = clamp(self.x,0,display_width)
			self.hit_sidewalls()
		#collisions with players, only for movement, the ball should keep going after playes are crashing
		if self.reached_player_position():
			self.hit_player()
		if draw:
			self.draw(gameDisplay)

def get_inputs(player1_movement):
    exit = False
    for event in pygame.event.get():
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                exit = True
            elif event.key == pygame.K_LEFT:
                player1_movement = -1
            elif event.key == pygame.K_RIGHT:
                player1_movement = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if player1_movement == -1:
                	player1_movement =0
            elif event.key == pygame.K_RIGHT:
                if player1_movement ==1:
                	player1_movement = 0
    return exit, player1_movement

def main():

	clock = pygame.time.Clock()
	pygame.init()
	font = pygame.font.Font(None, 30)
	gameDisplay = pygame.display.set_mode((display_width,display_height))
	pygame.display.set_caption('Pong')
	player_top = Player(0,bar_width,bar_height,black,None, movespeed = 20)
	player_bottom = perfect_player.perfect_player(1,display_width, display_height, bar_width,bar_height,black)
	ball = Ball(5,20,5,1,color = black)
	exit = False
	done = False
	while not exit:
		exit, player_top.direction= get_inputs(player_top.direction)
		gameDisplay.fill(white)
		player_top.update(gameDisplay)
		player_bottom.think(gameDisplay,ball)
		done = ball.update(gameDisplay)
		if done:
			ball = Ball(5,black, 20, 5,1)

		pygame.display.update()
		clock.tick(60)


if __name__ == "__main__":

    main()
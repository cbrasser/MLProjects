import pygame


class perfect_player:
	def __init__(self,position, display_width,display_height, width, height,color, movespeed=20):
		self.score = 0
		self.color = color
		self.movespeed = movespeed
		self.width = width
		self.height = height
		self.x = display_width/2 - width/2
		if position == 0:
			self.y = 0
		else:
			self.y = display_height - self.height
		


	def think(self,gameDisplay, ball, draw = True):
		if ball.x > self.x:
			self.update(1,gameDisplay, draw, ball.x)
		elif ball.x < self.x:
			self.update(-1, gameDisplay, draw, ball.x)

	def draw(self, gameDisplay):
		pygame.draw.rect(gameDisplay, self.color, [self.x,self.y,self.width,self.height])

	def update(self, direction, gameDisplay, draw = True, ball_x = 0):
		#Testing with a "perfect" perfect player for now that can just set his x to the x of the ball instead having to make a move decision
		self.x = ball_x - self.width/2
		#self.x += direction*self.movespeed
		if draw:
			self.draw(gameDisplay)

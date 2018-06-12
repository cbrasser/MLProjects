import pygame
import time
import random
import numpy as np
import pong
import genetic_algorithm
import neuralNetwork
import perfect_player

#--------------------Colors-----------------------
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)

#----------------------Sizes-----------------------
display_width = 1250
display_height = 750
player_width = 90
player_height = 10
x = display_width/2 - player_width/2
y = display_height - player_height 
ball_max_speed = 15
player_movespeed= 15

#--------------------Game variables-------------------

highscore = 0
gen= 0
totalPopulation = 50
bestPlayer = None
#(radius, color, max_speed,initial_speed, acceleration_per_bounce):
ball = pong.Ball(5, 20, ball_max_speed, 0,color=red)
allPlayers = []
activePlayers = []
counter = 0
#(position,width, height, color,brain,display_w = display_width, display_h=display_height, movespeed = 20):
bestPlayer = pong.Player(1,player_width, player_height,black,None,display_w=display_width, display_h=display_height, movespeed=player_movespeed)
#(self,position, display_width,display_height, width, height,color, movespeed=20):
opPlayer = perfect_player.perfect_player(0,display_width, display_height, player_width, player_height, black)


runBest = False

#----------------------Init------------------------
crashed = False
clock = pygame.time.Clock()
pygame.init()
font = pygame.font.Font(None, 30)
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong')

def setup():

	for i in range(0,totalPopulation):
		tmp_player = pong.Player(1,player_width, player_height,random_color(),None,display_w=display_width, display_h=display_height, movespeed=player_movespeed)
		activePlayers.append(tmp_player)
		allPlayers.append(tmp_player)

def toggleState():
	runBest != runBest

	if runBest:
		resetGame(bestPlayer, ball)
	else:
		bestPlayer, ball, activePlayers, allPlayers = next_generation(bestPlayer, ball, activePlayers, allPlayers)

def draw():
	global highscore
	global bestPlayer
	global activePlayers
	global ball
	global allPlayers
	global opPlayer
	global gen

	if runBest and instanceof(bestPlayer, pong.Player):
		bestPlayer.think(ball)
		bestPlayer.update()
		if ball.crashCheck(bestPlayer.x,bestPlayer.y):
			ga.resetGame()


	else:
		if len(activePlayers)>0:
			#iterating backwards so we dont run into out of bound exceptions
			for i in range(len(activePlayers)-1,-1,-1):
				tmp_player = activePlayers[i]
				tmp_player.think(ball)
				tmp_player.update(gameDisplay)
				#check for each player if he lost a game on the current frame
				#only check if the ball is currently at a y position where this is possible, aka y >= display_height
				if ball.y >= display_height-player_height:
					if not ball.check_player_collision(tmp_player):
						activePlayers.pop(i)
					else:
						tmp_player.score+=50


	tempHighscore = 0
	if not runBest:
		tempBestPlayer = None
		for i in range(0,len(activePlayers)):
			s = activePlayers[i].score
			if s > tempHighscore:
				tempHighscore = s
				tempBestPlayer = activePlayers[i]
		if tempHighscore > highscore:
			highscore = tempHighscore
			bestPlayer = tempBestPlayer
	else:
		tempHighscore = bestPlayer.score
		if tempHighscore >highscore:
			highscore = tempHighscore

	if runBest:
		bestPlayer.draw(gameDisplay)
	else:
		for i in range(0,len(activePlayers)):
			activePlayers[i].draw(gameDisplay)
		if len(activePlayers)==0:
			print("next generation, highscore: ",highscore)
			bestPlayer, ball, activePlayers, allPlayers = genetic_algorithm.next_generation(bestPlayer, ball, activePlayers, allPlayers)
			gen+=1

	ball.update(gameDisplay)
	opPlayer.think(gameDisplay,ball)

def check_for_termination():
	for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                	pygame.time.wait(10000)
                    
	return False

def random_color():
	return (random.randrange(255),random.randrange(255),random.randrange(255))

def show_fps(gameDisplay):
    text = font.render(str(int(clock.get_fps())), True, blue)
    gameDisplay.blit(text, (5,5))

def show_generation(gameDisplay):
	text = font.render("Generation: "+str(gen), True, blue)
	gameDisplay.blit(text, (5,30))

def show_current_highscore(gameDisplay):
	text = font.render("Highscore: "+str(highscore), True, blue)
	gameDisplay.blit(text, (5,55))

def show_agents_left(gameDisplay):
	text = font.render("Agents left: "+str(len(activePlayers)), True, blue)
	gameDisplay.blit(text, (5,80))

def main():
	setup()
	exit = False
    
	while not exit:
		gameDisplay.fill(white)
		exit = check_for_termination()
		draw()
		show_fps(gameDisplay)
		show_generation(gameDisplay)
		show_current_highscore(gameDisplay)
		show_agents_left(gameDisplay)
		pygame.display.update()
		clock.tick(60)




if __name__ == "__main__":
    main()










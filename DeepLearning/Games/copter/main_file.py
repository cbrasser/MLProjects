import pygame
import time
import random
import numpy as np
import copter
import ga
import neuralNetwork

#--------------------Colors-----------------------
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)

#----------------------Sizes-----------------------
display_width = 1600
display_height = 1200
x =  (display_width * 0.2)
y = (display_height * 0.5)

#--------------------Game variables-------------------

highscore = 0
totalPopulation = 10
bestCopter = None
wall = copter.Wall()
allCopters = []
activeCopters = []
counter = 0
bestCopter = copter.Copter(x,y,None)

runBest = False

#----------------------Init------------------------
crashed = False
clock = pygame.time.Clock()
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Copter')

def setup():

	for i in range(0,totalPopulation):
		tmp_copter = copter.Copter(x,y,None)
		activeCopters.append(tmp_copter)
		allCopters.append(tmp_copter)

def toggleState():
	runBest != runBest

	if runBest:
		resetGame(bestCopter, wall)
	else:
		bestCopter, wall, activeCopters, allCopters = next_generation(bestCopter, wall, activeCopters, allCopters)

def draw():
	global highscore
	global bestCopter
	global activeCopters
	global wall
	global allCopters

	if runBest and instanceof(bestCopter, copter.Copter):
		bestCopter.think(wall)
		bestCopter.update()
		if wall.crashCheck(bestCopter.x,bestCopter.y):
			ga.resetGame()


	else:

		if len(activeCopters)>0:
			#iterating backwards so we dont run into out of bound exceptions
			for i in range(len(activeCopters)-1,-1,-1):
				tmp_copter = activeCopters[i]
				tmp_copter.think(wall)
				tmp_copter.update(gameDisplay)
				if wall.crashCheck(tmp_copter.x,tmp_copter.y):
					activeCopters.pop(i)


	tempHighscore = 0
	if not runBest:
		tempBestCopter = None
		for i in range(0,len(activeCopters)):
			s = activeCopters[i].score
			if s > tempHighscore:
				tempHighscore = s
				tempBestCopter = activeCopters[i]
		if tempHighscore > highscore:
			highscore = tempHighscore
			bestCopter = tempBestCopter
	else:
		tempHighscore = bestCopter.score
		if tempHighscore >highscore:
			highscore = tempHighscore

	if runBest:
		bestCopter.draw(gameDisplay)
	else:
		for i in range(0,len(activeCopters)):
			activeCopters[i].draw(gameDisplay)
		if len(activeCopters)==0:
			print("next generation, highscore: ",highscore)
			bestCopter, wall, activeCopters, allCopters = ga.next_generation(bestCopter, wall, activeCopters, allCopters)

	wall.update(gameDisplay)

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

def main():
	setup()
	exit = False
    
	while not exit:
		gameDisplay.fill(white)
		exit = check_for_termination()
		draw()
		pygame.display.update()
		clock.tick(60)




if __name__ == "__main__":
    main()










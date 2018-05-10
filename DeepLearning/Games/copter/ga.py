import copter
import random



def resetGame(bestCopter, wall):
	counter = 0
	if bestCopter:
		bestCopter.score = 0
	wall = copter.Wall()
	return bestCopter, wall


def next_generation(bestCopter, wall,activeCopters, allCopters):
	bestCopter, wall  =resetGame(bestCopter, wall)
	normalize_fitness(allCopters)
	activeCopters = generate(allCopters)
	allCopters = activeCopters[:]
	return bestCopter, wall, activeCopters, allCopters


def generate(oldCopters):
	newCopters = []
	for i in range(0,len(oldCopters)):
		tmp_copter = poolSelection(oldCopters)
		newCopters.append(tmp_copter)
	return newCopters

def normalize_fitness(copters):
	for i in range(0,len(copters)):
		copters[i].score = pow(copters[i].score,2)

	sum = 0
	for i in range(0,len(copters)):
		sum += copters[i].score
	for i in range(0, len(copters)):
		copters[i].fitness = copters[i].score / sum

def poolSelection(copters):
	index =0
	r = random.randrange(1)

	while r>0:
		r -= copters[index].fitness
		index+=1

	index-=1

	return copters[index].copy()

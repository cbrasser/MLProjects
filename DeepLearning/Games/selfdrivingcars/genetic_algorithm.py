import car
import random

def resetGame(bestCar):
	counter = 0
	if bestCar:
		bestCar.score = 0
	return bestCar


def next_generation(bestCar,activeCars, allCars):
	bestCar =resetGame(bestCar)
	normalize_fitness(allCars)
	activeCars = generate(allCars)
	allCars = activeCars[:]
	return bestCar,activeCars, allCars


def generate(oldCars):
	newCars = []
	for i in range(0,len(oldCars)):
		tmp_car = poolSelection(oldCars)
		newCars.append(tmp_car)
	return newCars

def normalize_fitness(cars):
	for i in range(0,len(cars)):
		car[i].score = pow(cars[i].score,2)

	sum = 0
	for i in range(0,len(cars)):
		sum += cars[i].score
	for i in range(0, len(cars)):
		cars[i].fitness = cars[i].score / sum

def poolSelection(cars):
	index =0
	r = random.randrange(1)

	while r>0:
		r -= cars[index].fitness
		index+=1

	index-=1

	return cars[index].copy()

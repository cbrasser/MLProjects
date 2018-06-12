import pong
import random


def resetGame(bestPlayer, ball):
	counter = 0
	if bestPlayer:
		bestPlayer.score = 0
	ball = pong.Ball(5, 20, 15, 0)
	return bestPlayer, ball


def next_generation(bestPlayer, ball,activePlayers, allPlayers):
	bestPlayer, ball  =resetGame(bestPlayer, ball)
	normalize_fitness(allPlayers)
	activePlayers = generate(allPlayers)
	allPlayers = activePlayers[:]
	return bestPlayer, ball, activePlayers, allPlayers


def generate(oldPlayers):
	newPlayers = []
	for i in range(0,len(oldPlayers)):
		tmp_player = poolSelection(oldPlayers)
		newPlayers.append(tmp_player)
	return newPlayers

def normalize_fitness(players):
	for i in range(0,len(players)):
		players[i].score = pow(players[i].score,2)

	sum = 0
	for i in range(0,len(players)):
		sum += players[i].score
	for i in range(0, len(players)):
		players[i].fitness = players[i].score / sum

def poolSelection(players):
	index =0
	r = random.randrange(1)

	while r>0:
		r -= players[index].fitness
		index+=1

	index-=1

	return players[index].copy()

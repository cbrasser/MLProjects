import gym
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter

#Learning rate
LR = 1e-3
env = gym.make('CartPole-v0')
env.reset()
goal_steps = 500
score_requirement = 50
initial_games = 10000

def some_random_games_first():
    for episode in range(500):
        env.reset()
        for t in range(goal_steps):
            #Can be left out to speed up, only visuals
            env.render()
            action = env.action_space.sample()
            #Data from the game (zB. Pole, car, ...), score, bool, info
            observation, reward, done, info = env.step(action)
            if done:
                break

some_random_games_first

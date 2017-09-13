import cars.py
import numpy as np
import random
import neuralNet


e = 1
max_score =0
score =0
i=0
random_initial_games = 1000


def train_model(model, params):

    goal_frames = 1000

    while i < goal_frames:
        i+=1

    if random.random < e or i < random_initial_games:
        move = np.random.randint()

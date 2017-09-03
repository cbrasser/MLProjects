import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import copter

#Learning rate
LR = 1e-3
#copter.setUp()
goal_steps = 500
score_requirement = 50
initial_games = 100
action = 0

def some_random_games_first():
    for episode in range(500):
        copter.reset()
        for t in range(goal_steps):
            global action
            #Can be left out to speed up, only visuals
            #copter.render()
            action = copter.random_action(action)
            #Data from the game (zB. Pole, car, ...), score, bool, info
            observation, reward, done = copter.main_game_loop(action)
            if done:
                break

#some_random_games_first()

def initial_population():
    training_data = [] # initial data will be random
    scores = []
    accepted_scores = []

    for _ in range(initial_games):
        score = 0
        game_memory=[]
        prev_observation = []
        for _ in range(goal_steps):
            global action
            #Only generates 0s and 1s
            action = copter.random_action(action)
            observation, reward, done = copter.main_game_loop(action)

            game_memory.append([observation,action])

            score += reward
            if done:
                break
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                #Output in this form because of one-hot, could be useful when there are more input possibilities
                #than just 0 or 1!
                if data[1] == 1:
                    output = [0,1]
                elif data[1] == 2:
                    output = [1,0]
                else:
                    output = [0,0]

                # saving our training data
                training_data.append([data[0], output])
        copter.reset()
        scores.append(score)

    training_data_save = np.array(training_data)
    np.save('saved.npy', training_data_save)

    print('Average accepted score: ',mean(accepted_scores))
    print('Median accepted score: ', median(accepted_scores))
    print(Counter(accepted_scores))

    print('TRAINGING DATA',training_data[0])
    print('TRAINGING DATA',training_data[0][0])

    return training_data


def neural_network_model(input_size):
    network = input_data(shape=[None, input_size, 1], name = 'input')

    network = fully_connected(network, 128, activation = 'relu')
    #0.8 is keep rate rather than dropout rate ??
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation = 'relu')

    network = fully_connected(network, 256, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 2, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name ='targets')
    model = tflearn.DNN(network, tensorboard_dir ='log')

    return model

def train_model(training_data, model=False):
    # i contains [observations, output (action you took)]
    print(len(training_data[0][0]))
    X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
    y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(input_size=len(X[0]))

    model.fit({'input': X}, {'targets': y}, n_epoch=3, snapshot_step=500, show_metric=True, run_id='openai_learning')

    return model

training_data = initial_population()
model = train_model(training_data)

'''
model.save('myModel.model')

model.load('myModel.model')
'''
scores = []
choices = []
for each_game in range(100):
    score = 0
    game_memory =[]
    prev_obs = []
    copter.reset()
    for _ in range((goal_steps)):
        global action
        #copter.render()
        if len(prev_obs) ==0:
            action = copter.random_action(action)
        else:
            action = np.argmax(model.predict(prev_obs)[0])
        choices.append(action)

        new_observation, reward, done = copter.main_game_loop(action)
        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score += reward
        if done:
            break
    scores.append(score)

print('Average score: ',sum(scores)/len(scores))

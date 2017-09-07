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
env = gym.make('CartPole-v1')
env.reset()
goal_steps = 500
score_requirement = 50
initial_games = 1000

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
            #Only generates 0s and 1s
            action = random.randrange(0,2)
            observation, reward, done, info = env.step(action)
            print('obs: ',observation)
            if len(prev_observation) > 0:
                #Action is either 0 or 1
                game_memory.append([prev_observation,action])

            prev_observation = observation

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
                elif data[1] == 0:
                    output = [1,0]

                # saving our training data
                training_data.append([data[0], output])
        env.reset()
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
    network = dropout(network, 0.8)

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
    X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
    y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(input_size=len(X[0]))

    model.fit({'input': X}, {'targets': y}, n_epoch=3, snapshot_step=500, show_metric=True, run_id='openai_learning')

    return model

training_data = initial_population()
model = train_model(training_data)


model.save('myModel.model')

#model.load('myModel.model')


scores = []
choices = []
for each_game in range(100):
    score = 0
    game_memory =[]
    prev_obs = []
    env.reset()
    for _ in range((goal_steps)):
        env.render()
        if len(prev_obs) ==0:
            action = random.randrange(0,2)
        else:
            action = np.argmax(model.predict(prev_obs.reshape(-1, len(prev_obs),1))[0])
        choices.append(action)

        new_observation, reward, done, info = env.step(action)
        prev_obs = new_observation
        game_memory.append([new_observation, action])
        score += reward
        if done:
            break
    scores.append(score)

print('Average score: ',sum(scores)/len(scores))



























#

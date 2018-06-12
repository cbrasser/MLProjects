import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import math
import json
import pickle

#Learning rate
LR = 0.0001
#copter.setUp()
goal_steps = 500
score_requirement = 50
initial_games = 1000

class ActivationFunction:
    def __init__(self, func, dfunc):
        self.func = func
        self.dfunc = dfunc

def sigmoid1(x):
    if x< 0:
        return 1- 1/(1 +math.exp(x))
    else:
        return 1/(1 +math.exp(-x))


sigmoid = ActivationFunction(sigmoid1, lambda y : y*(1-y))

class NeuralNetwork:
    def __init__(self, a, b,c):
        if isinstance(a, NeuralNetwork):
            self.input_nodes = a.input_nodes
            self.hidden_nodes = a.hidden_nodes
            self.output_nodes = a.output_nodes

            self.weights_ih = np.copy(a.weights_ih)
            self.weights_ho = np.copy(a.weights_ho)

            self.bias_h = np.copy(a.bias_h)
            self.bias_o = np.copy(a.bias_o)

        else:
            self.input_nodes = a
            self.hidden_nodes = b
            self.output_nodes = c

            self.weights_ih = np.random.random((self.hidden_nodes, self.input_nodes))*2 -1
            self.weights_ho = np.random.random((self.output_nodes, self.hidden_nodes)) *2 -1

            self.bias_h = np.random.random((self.hidden_nodes, 1))
            self.bias_o = np.random.random((self.output_nodes, 1))

        self.set_learning_rate()
        self.set_activation_function()

    def predict(self, input_array):
        f = np.vectorize(self.activation_function.func)
        inputs = np.transpose(np.mat(input_array))
        hidden = np.dot(self.weights_ih,inputs)
        hidden +=self.bias_h
        hidden = f(hidden)
        output = self.weights_ho * hidden
        output +=self.bias_o
        output = f(output)
        return np.array(output)

    def set_learning_rate(self, learning_rate = 0.1):
        self.learning_rate = learning_rate

    def set_activation_function(self, func = sigmoid):
        self.activation_function = func

    def train(self, input_array, target_array):
        f = np.vectorize(self.activation_function.func)
        df = np.vectorize(self.activation_function.dfunc)
        inputs = np.mat(input_array)
        hidden = self.weights_ih * inputs
        hidden.append(self.bias_h)
        hidden = f(hidden)

        outputs = self.weights_ho * hidden
        outputs.append(self.bias_o)
        outputs = f(outputs)

        targets = np.mat(target_array)
        output_errors = targets - output
        gradients = df(outputs)
        gradients = gradients*output_errors
        gradients = gradients * self.learning_rate

        hidden_T = np.transpose(hidden)
        weight_ho_deltas = gradients * hidden_T

        self.weights_ho += weight_ho_deltas
        self.bias_o += gradients

        who_t = np.transpose(self.weights_ho)
        hidden_errors = who_t * output_errors

        hidden_gradient = df(hidden)
        hidden_gradient *=hidden_errors
        hidden_gradient *= self.learning_rate

        inputs_T = np.transpose(inputs)
        weight_ih_deltas = hidden_gradient * inputs_T

        self.weights_ih += weight_ih_deltas
        self.bias_h +=hidden_gradient

    def serialize(self):
        return JSON.stringify(self)

    def deserialize(data):
        data = JSON.parse(data)

        nn = NeuralNetwork(data.input_nodes, data.hidden_nodes, data.output_nodes)
        nn.weights_ih = JSON.parse(data.weights_ih);
        nn.weights_ho = JSON.parse(data.weights_ho);
        nn.bias_h = JSON.parse(data.bias_h);
        nn.bias_o = JSON.parse(data.bias_o);
        nn.learning_rate = data.learning_rate;
        return nn;

    def copy(self):
        return NeuralNetwork(self, self.hidden_nodes, self.output_nodes)

    def mutate(self, func):
        f = np.vectorize(func)
        self.weights_ih = f(self.weights_ih)
        self.weights_ho = f(self.weights_ho)
        self.bias_h = f(self.bias_h)
        self.bias_o = f(self.bias_o)


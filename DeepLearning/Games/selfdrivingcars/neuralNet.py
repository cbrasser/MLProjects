from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tflearn


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

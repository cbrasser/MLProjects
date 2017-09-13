from keras.model import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback
import tensorflow as tf

tf.python.control_flow_ops = tf

def neural_net(num_sensors, params, load=''):
    model = Sequential()

    # First layer.
    model.add(Dense(
        params[0], init='lecun_uniform', input_shape=(num_sensors,)
    ))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Second layer.
    model.add(Dense(params[1], init='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    # Output layer.
    model.add(Dense(3, init='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)

    if load:
        model.load_weights(load)

    return model

def lstm_net(num_sensors, load=False):
    model = Sequential()
    model.add(LSTM(
        output_dim=512, input_dim=num_sensors, return_sequences=True
    ))
    model.add(Dropout(0.2))
    model.add(LSTM(output_dim=512, input_dim=512, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=3, input_dim=512))
    model.add(Activation("linear"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop")

    return model

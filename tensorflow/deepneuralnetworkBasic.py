import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#TODO: Summarize and read up that stuff
#Input data  -> weight ->  Hidden Layer 1 -> Activation function -> Weights
#-->Hidden layer 2 -->Activation function --> .......... -->Output Layer

#Compare output to intendet output with cost (lost) function (cross entropy)
#optimizer function to minimize cost (AdamOptimizer, SGD, AdaGRad, ....)

#Backpropagation
#Feed forward + Backpropagation = epoch

#one_hot = one is off, rest is off..
mnist = input_data.read_data_sets("/tmp/data", one_hot=True)

#10 classes in dataset, 0-9
#One_hot outputs data in form [0,1,0,0,0,0,0,0,0,0]
#Where 1 denotes the category a datapoint belongs to

#We have 3 hidden layers with each 500 nodes, could be whatever we want
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10
#batches of 100 features at a time
batch_size = 100


x = tf.placeholder('float') # Data
y = tf.placeholder('float') # Label of that data

def neural_network_model(data):
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([784,n_nodes_hl1])),
                        'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}
                        #input_data * weight + bias
                        #Bias
    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1,n_nodes_hl2])),
                        'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}
    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2,n_nodes_hl3])),
                        'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}
    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3,n_classes])),
                        'biases': tf.Variable(tf.random_normal([n_classes]))}

    #Model for each layer: input_data * weight + bias
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    #Activation function
    l1 =tf.nn.relu(l1)

    #Pass the data through the layers

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 =tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 =tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights'])+ output_layer['biases']
    return output

#Model done at this point, now we need to tell tf what to do with this model

def train_neural_network(x):
    prediction = neural_network_model(x)

    cost= tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y))
    #Like stochastic gradient descent
    #Standard learning rate = 0.001
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    #Cycle of feed forward + Backpropagation
    hm_epochs = 10

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        #Now the session has started, done with defining variables etc
        #Here we are training
        for epoch in range(hm_epochs):
            epoch_loss = 0
            #_ : Variable we dont care about
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x,epoch_y = mnist.train.next_batch(batch_size)
                #Optimizing cost by adjusting the weights (tf high-level stuff)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
            print('Epoch', epoch, 'completed out of', hm_epochs, 'loss: ',epoch_loss)


        #Compate prediction to actual label
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('accuracy: ',accuracy.eval({x: mnist.test.images, y:mnist.test.labels}))

train_neural_network(x)

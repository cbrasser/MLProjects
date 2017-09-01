import tensorflow as tf

#Computation graph where you model everything
#Nodes, attribute, features, labels etc.

x1 = tf.constant(5)
x2 = tf.constant(6)

#"define a model that multiplies 5 and 6"
#Is not actually calcing something
result = tf.multiply(x1,x2)

with tf.Session() as sess:
    output = sess.run(result)
    print(output)

#session saved in a python variable output
print(output)

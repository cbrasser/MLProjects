import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors
import numpy as np

#Get data
df = pd.read_csv('abalone.data.txt')

#Build 2 Lists of data, X without the classification attribute (e.g. Sex)
#and y with only the classification attribute
X = np.array(df.drop(['sex'],1))
y = np.array(df['sex'])

#Split both lists into a train and a test part
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

clf = neighbors.KNeighborsClassifier()
#Train the Model with the train part of the data and the corresponding classifiers
clf.fit(X_train,y_train)

#Let the Model predict the classes of all datasets in the X_test list
#and check correctness with the y_test set, calc accuracy from the ratio
accuracy = clf.score(X_test,y_test)


# example_measure = np.array([[0.24,0.14,0.8,0.7,0.388,0.587,0.13,5],[0.44,0.34,0.1,0.451,0.188,0.087,0.13,10]])
# example_measure = example_measure.reshape(len(example_measure),-1)
# prediction = clf.predict(example_measure)
#print(prediction)

print(accuracy)

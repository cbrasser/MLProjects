import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd

df = pd.read_csv('breast-cancer-wisconsin.data.txt')
df.replace('?',-99999,inplace = True)

#Remove id since its clearly noise and not related to data
df.drop(['id'],1,inplace=True)

X = np.array(df.drop(['class'],1))
y = np.array(df['class'])

#Separate data into training and testing
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y, test_size=0.2)

clf = neighbors.KNeighborsClassifier()
clf.fit(X_train,y_train)

accuracy = clf.score(X_test, y_test)
print(accuracy)

example_measure = np.array([[4,2,1,1,1,2,3,2,1],[4,2,1,2,2,2,3,2,1],[9,9,9,9,2,2,3,2,1]])

#first attribute is amount of measures in the list of samples, shapes data for sklearn
example_measure = example_measure.reshape(len(example_measure),-1)

prediction = clf.predict(example_measure)
print(prediction)

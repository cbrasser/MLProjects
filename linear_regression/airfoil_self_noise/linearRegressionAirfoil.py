import pandas as pd
import quandl, math, datetime, time
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

df = pd.read_csv('airfoil_self_noise.dat.txt',sep='\t')

print(df.head())

X = np.array(df.drop(['sound'],1))
y = np.array(df['sound'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

clf = LinearRegression()

clf.fit(X_train, y_train)

with open('linearRegression.pickle','wb') as f:
    pickle.dump(clf, f)

pickle_in = open('linearRegression.pickle','rb')
clf = pickle.load(pickle_in)

accuracy = clf.score(X_test,y_test)

print(accuracy)

import pandas as pd
import quandl, math, datetime, time
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('ggplot')

df = quandl.get('WIKI/GOOGL')
#Get the right data from the dataframe
df = df[['Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100

df = df[['Adj. Close','HL_PCT','PCT_change','Adj. Volume']]


forecast_col = 'Adj. Close'

#Fill in empty fields
df.fillna(-99999, inplace = True)

#Builds an integer that defines the amount of days we want to forecast
#Example: wa have 300 datapoints, forecast_out will be 0.01 * 300 = 3 day
forecast_out = int(math.ceil(0.01*len(df)))
print(forecast_out)

#The label values are the Adj. Close value from the datapoints forecast_out days in the future
df['label'] = df[forecast_col].shift(-forecast_out)



#Capital X for features
#Array of all values except label column
X = np.array(df.drop(['label'],1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]


df.dropna(inplace = True)
#lower case y for lables
#Array with all values of label column
y = np.array(df['label'])


#Splits the data into a train and a test part, test part size can be handed
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs = 10) #Algorithm used, can be easy switched

#Why train and test on different data ? - Else it already knows the data from training
clf.fit(X_train, y_train) #actual training

#Store classifier in Filesystem
with open('linearRegression.pickle','wb') as f:
    pickle.dump(clf, f)

pickle_in = open('linearRegression.pickle','rb')
clf = pickle.load(pickle_in)

accuracy = clf.score(X_test, y_test) #test, accuracy is squared error
#print(accuracy)

forecast_set = clf.predict(X_lately)

print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan

#Set up for ploting
last_date = df.iloc[-1].name
last_unix = time.mktime(last_date.timetuple())
one_day  = 86400
next_unix = last_unix + one_day

#
for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    #
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

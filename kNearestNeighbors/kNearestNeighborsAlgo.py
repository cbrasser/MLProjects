from math import sqrt
import numpy as np
import pandas as pd
import random
import warnings
from collections import Counter


#Take all datapoints in the data param (including the group they belong to)
#and one datapoint to predict it's group.
#Go through every datapoint in data and calc the distance from the predict datapoint to this one.
#Build list with all distances and the group their point belongs to
#Check to which group the k nearest points belong to and return the group with more votes
def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('K is set to be a value less than total voting groups, idiot!')

    #Calc the distances from the predict datapoint to all features in all groups (e.g. k & r)
    distances = []
    for group in data:
        for feature in data[group]:
            #euclidian distance vai vector norm
            euclidian_distance = np.linalg.norm(np.array(feature)-np.array(predict))
            distances.append([euclidian_distance, group])

    #We can drop every distance beyond the k-nearest since only those interest us
    votes = [i[1] for i in sorted(distances) [:k]]
    #Only take the first (1) one
    vote_result  = Counter(votes).most_common(1)[0][0]
    confidence = float(Counter(votes).most_common(1)[0][1]) / k
    #print(vote_result, confidence)
    return vote_result, confidence

accuracies = []
for i in range(25):

    df = pd.read_csv('breast-cancer-wisconsin.data.txt')
    df.replace('?',-99999, inplace=True)
    df.drop(['id'],1 , inplace=True)
    #List of lists with all data as floats
    full_data = df.astype(float).values.tolist()

    random.shuffle(full_data)

    test_size = 0.2
    train_set = {2:[], 4:[]}
    test_set = {2:[], 4:[]}
    #Split data into train and test set
    train_data = full_data[:-int(test_size*len(full_data))]
    test_data = full_data[-int(test_size*len(full_data)):]

    #Build dictionaries for k_nearest function
    for i in train_data:
        train_set[i[-1]].append(i[:-1])

    for i in test_data:
        test_set[i[-1]].append(i[:-1])

    correct = 0
    total = 0
    #Go trough every datapoint of all groups in the test set
    #For each datapoint calculate the vote for the group and the confidence of the vote
    #This is done via the train_set every time
    for group in test_set:
        for data in test_set[group]:
            vote, confidence = k_nearest_neighbors(train_set, data, k=5)
            if group == vote:
                correct += 1
            else:
                print(confidence)
            total +=1

    accuracies.append(float(correct)/total)

#Print average accuracy
print(sum(accuracies)/len(accuracies))


# [[plt.scatter(ii[0], ii[1], s=100, color=i) for ii in dataset[i]] for i in dataset]
# plt.scatter(new_feature[0],new_feature[1], color=result)
# plt.show();

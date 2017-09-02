'''
lexicon = [chair, table, process, television]

Some random sentence to process

[0     0      0       0    1]

Our lexicon will be consisting out of every word in the entire dataset,
that way we can build an array of 0s & 1s like above to have uniform datapoints
and we dont need to worry about difference in sentence length etc.
'''

import nltk
from nltk.tokenize import word_tokenize
#Information on natural language processing on sentdex website
from nltk.stem import WordNetLemmatizer
import numpy as np
import random
import pickle
from collections import Counter

lemmatizer = WordNetLemmatizer
hm_lines = 1000000

#Read data and stuff into lexicon
def create_lexicon(pos, neg):
    lexicon = []
    with open(pos, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            all_words = word_tokenize(l.lower())
            lexicon += list(all_words)

    with open(neg, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            all_words = word_tokenize(l.lower())
            lexicon += list(all_words)

    #lexicon = [lemmatizer.lemmatize(i,pos[0].lower()) for i,pos in nltk.pos_tag(lexicon)]
    #lexicon = [lemmatizer.lemmatize(i,'v') for i in lexicon]
    w_counts = Counter(lexicon)
    #w_counts will be like {'the: '3453, 'and': 20344}
    l2 = []
    #Eliminate words that appear between 50 and 1000 times (etc. 'and', 'or', ...)
    for w in w_counts:
        if 1000 > w_counts[w] > 50:
            l2.append(w)
    print(len(l2))
    return l2

def sample_handling(sample, lexicon, classification):
    featureset = []
    '''
    featureset = [
    [[indexes of features],[pos neg]],
    [[ 0 1 1 1 0 0  0],[0 1]],
    ...
    ]
    '''
    with open(sample, 'r') as f:
        contents = f.readlines()
        for l in contents[:hm_lines]:
            current_words = word_tokenize(l.lower())
            #current_words = [lemmatizer.lemmatize(i,pos[0].lower()) for i,pos in  nltk.pos_tag(current_words)]
            #current_words = [lemmatizer.lemmatize(i,'v') for i in current_words]
            #Init features on zero
            features = np.zeros(len(lexicon))
            for word in current_words:
                if word.lower() in lexicon:
                    indexd_value = lexicon.index(word.lower())
                    features[indexd_value] += 1
            features = list(features)
            featureset.append([features, classification])
    return featureset

def create_feature_sets_and_labels(pos, neg, test_size=0.1):
    lexicon = create_lexicon(pos, neg)
    features = []
    features += sample_handling('pos.txt', lexicon,[1,0])
    features += sample_handling('neg.txt', lexicon,[0,1])
    #Shuffling really important, else the neural network might really havy bias
    random.shuffle(features)

    features = np.array(features)

    testing_size = int(test_size*len(features))
    #:,0 --> all 0th elements in a list of lists1
    #Because first element in features is list of dfeatures we get the list of features
    train_x = list(features[:,0][:-testing_size])
    train_y = list(features[:,1][:-testing_size])

    test_x = list(features[:,0][-testing_size:])
    test_y = list(features[:,1][-testing_size:])

    return train_x, train_y, test_x, test_y


if __name__ == '__main__':
    train_x,train_y,test_x,test_y = create_feature_sets_and_labels('pos.txt', 'neg.txt')
    with open('sentiment_set.pickle','wb') as f:
        pickle.dump([train_x,train_y,test_x,test_y], f)






































    #

import numpy as np
import pickle
import os
import feature_extract

#loading all required files
fileObject1 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vecdict.p'), 'r')
fileObject2= open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'classif.p'), 'r')
vec = pickle.load(fileObject1)
classifier = pickle.load(fileObject2)
fileObject1.close()
fileObject2.close()

def tweetscore(sentence):
    features = feature_extract.get_features(sentence)
    features_vec = vec.transform(features)
    score = classifier.decision_function(features_vec)[0]
    percentage = int(round(2.0*(1.0/(1.0+np.exp(-score))-0.5)*100.0))
    #print "score is ",percentage
    return percentage

def isSarcastic(sentence):
    features = feature_extract.get_features(sentence)
    features_vec = vec.transform(features)
    score = classifier.decision_function(features_vec)
    print "score is %d",score
    percentage = int(round(2.0 * (1.0 / (1.0 + np.exp(-score)) - 0.5) * 100.0))
    #print "Predicted Class Is (0: Non-Sarcastic and 1: Sarcastic) ",percentage
    return percentage

#this method is called for prediction of sentence
def modelPredict(message):
    is_sarcastic=isSarcastic(message)
    #return percentage_sarcasm
    print is_sarcastic
    return is_sarcastic
import numpy as np
import scipy as sp
from sklearn.utils import shuffle
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction import DictVectorizer
import pickle
import feature_extract
import heapq

pos_data = np.load('posproc.npy')
neg_data = np.load('negproc.npy')
class_set = ['Non-Sarcastic', 'Sarcastic']
featuresets = []

index = 0
for tweet in pos_data:
    if (np.mod(index, 10000) == 0):
        print "Positive tweet processed: ", index
    featuresets.append((feature_extract.dialogue_act_features(tweet), class_set[1]))
    index += 1

index = 0
for tweet in neg_data:
    if (np.mod(index, 10000) == 0):
        print "Negative tweet processed: ", index
    featuresets.append((feature_extract.dialogue_act_features(tweet), class_set[0]))
    index += 1

featuresets = np.array(featuresets)
targets = (featuresets[0::, 1] == 'Sarcastic').astype(int)
vec = DictVectorizer()
featurevec = vec.fit_transform(featuresets[0::, 0])

file_Name = "vecdict.p"
fileObject = open(file_Name, 'wb')
pickle.dump(vec, fileObject)
fileObject.close()

print 'Splitting Data Set for Training and Testing ...'
order = shuffle(range(len(featuresets)))
targets = targets[order]
featurevec = featurevec[order, 0::]
size = int(len(featuresets) * .3)  # 30% is used for the test set

trainvec = featurevec[size:, 0::]
train_targets = targets[size:]
testvec = featurevec[:size, 0::]
test_targets = targets[:size]

print 'Training the model .....'
pos_p = (train_targets == 1)
neg_p = (train_targets == 0)
ratio = np.sum(neg_p.astype(float)) / np.sum(pos_p.astype(float))
new_trainvec = trainvec
new_train_targets = train_targets
for j in range(int(ratio - 1.0)):
    new_trainvec = sp.sparse.vstack([new_trainvec, trainvec[pos_p, 0::]])
    new_train_targets = np.concatenate((new_train_targets, train_targets[pos_p]))

#model support vector classifier
classifier = LinearSVC(C=0.1, penalty='l2', dual=True)
classifier.fit(new_trainvec, new_train_targets)

# Saving the classifier - pickle dump - serializing
file_Name = "classif.p"
fileObject = open(file_Name, 'wb')
pickle.dump(classifier, fileObject)
fileObject.close()

#testing/predicting
output = classifier.predict(testvec)
print "final result: ",classification_report(test_targets, output, target_names=class_set)

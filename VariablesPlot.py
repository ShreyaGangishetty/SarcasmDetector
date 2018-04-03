'''This class is used to analyze which feature has most important score for predicting a sentence.'''

import matplotlib.pyplot as plt
import os
import pickle
import numpy as np

def plot_coefficients(classifier, feature_names, top_features=20):
    coef = classifier.coef_.ravel()
    top_positive_coefficients = np.argsort(coef)[-top_features:]
    top_negative_coefficients = np.argsort(coef)[:top_features]
    top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    plt.figure(figsize=(20, 20))
    colors = ["red" if c < 0 else "blue" for c in coef[top_coefficients]]
    plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(1, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha="right")
    plt.show()

fileObject1 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vecdict.p'), 'r')
fileObject2= open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'classif.p'), 'r')
vec = pickle.load(fileObject1)
classifier = pickle.load(fileObject2)

feature_names=vec.get_feature_names()
top_only = []
for element in feature_names:
    print "element: ", element
    if "contains" not in str(element):
        print "appending"
        top_only.append(element)

#printing only top features/elements
print "top_only", top_only
plot_coefficients(classifier, top_only)
fileObject1.close()
fileObject2.close()
#plot_coefficients(classifier,)
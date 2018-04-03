"""This module is mainly used for extracting features for traning our model"""

import nltk
import numpy as np
import string
import load_sent
from textblob import TextBlob
import exp_replace

def get_features(sentence):
    features = {}
    grams_feature(features, sentence)
    sent_feature(features, sentence)
    return features


def grams_feature(features, sentence):
    sentence_reg = exp_replace.replace_reg(sentence)


    tokens = nltk.word_tokenize(sentence_reg)
    tokens = [porter.stem(t.lower()) for t in tokens]
    bigrams = nltk.bigrams(tokens)
    bigrams = [tuple[0] + ' ' + tuple[1] for tuple in bigrams]
    ngrams = tokens + bigrams

    for tup in ngrams:
        features['contains(%s)' % tup] = 1.0


def sent_feature(features, sentence):
    sentence_sentiment = exp_replace.replace_emo(sentence) ## :) is replaced by good and :( is replaced by sad
    tokens = nltk.word_tokenize(sentence_sentiment)
    tokens = [(t.lower()) for t in tokens]

    mean_sentiment = sentiments.score_sentence(tokens)
    features['Positive sentiment'] = mean_sentiment[0]
    features['Negative sentiment'] = mean_sentiment[1]
    features['Sentiment'] = mean_sentiment[0] - mean_sentiment[1]

    # TextBlob sentiment analysis for full sentence
    try:
        blob = TextBlob(
            "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip())
        features['BlobSentiment'] = blob.sentiment.polarity
    except:
        features['BlobSentiment'] = 0.0
  
    # Splitting the sentence into 2 parts and then calculating sentiment analysis on the sentence
    if len(tokens) == 1:
        tokens += ['.']
    f_half = tokens[0:len(tokens) / 2]
    s_half = tokens[len(tokens) / 2:]

    mean_sentiment_f = sentiments.score_sentence(f_half)
    features['PosSentiment1/2'] = mean_sentiment_f[0]
    features['Negsentiment1/2'] = mean_sentiment_f[1]
    features['Sentiment1/2'] = mean_sentiment_f[0] - mean_sentiment_f[1]

    mean_sentiment_s = sentiments.score_sentence(s_half)
    features['PosSentiment2/2'] = mean_sentiment_s[0]
    features['NegSentiment2/2'] = mean_sentiment_s[1]
    features['Sentiment2/2'] = mean_sentiment_s[0] - mean_sentiment_s[1]

    features['SentimentContrast'] = np.abs(features['Sentiment 1/2'] - features['Sentiment 2/2'])

    # TextBlob sentiment analysis for bith the halves
    try:
        blob = TextBlob(
            "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in f_half]).strip())
        features['BlobSentiment1/2'] = blob.sentiment.polarity
     except:
        features['BlobSentiment1/2'] = 0.0
    try:
        blob = TextBlob(
            "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in s_half]).strip())
        features['BlobSentiment2/2'] = blob.sentiment.polarity
    except:
        features['BlobSentiment2/2'] = 0.0
        features['BlobSubjectivity2/2'] = 0.0

    features['BlobSentimentContrast'] = np.abs(features['BlobSentiment1/2'] - features['BlobSentiment2/2'])
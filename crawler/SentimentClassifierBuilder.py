#!/usr/bin/env python

# This file runs on train.csv dataset (Sentiment140 dataset from Kaggle)
#  and builds a classification model
#
#       1. Logistic Regression Model
#             It saves classifier.joblib and tokenizer.joblib
#             which is loaded during test
#      2. A Logistic Regression Model
#             That uses trigrams to represent tweets and uses a
#             TFIDF vectorizer. It saves the model and tokenizer
#             to classifier_ngram_tfidf and tokenizer_ngram_tfidf.joblib
#      3. Deep Learning LSTM based model
#             model_deep_learning.joblib
#             tokenizer_deep_learning.joblib

import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras import layers

import numpy as np
import pandas as pd
from joblib import dump, load
from keras.layers import LSTM

stopwords = set(stopwords.words('english'))
tweet_tokenizer = TweetTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()


# trains the logistic regression model for classifying tweets as positive or negative
def train_model():
    corpus = r"train.csv"
    dataframe = pd.read_csv(corpus, header=None, usecols=[0, 5], encoding= "ISO-8859-1", names=['label', 'sentence'],)

    # shuffle the data frame as the dataset is sorted by labels
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)

    tweets = dataframe['sentence'].values
    labels = dataframe['label'].values

    # partition data into train, dev and test sets
    # the training data contains 1.6 million records so only 40000
    # is used in creation of the classification model
    tweets_train, y_train = tweets[:32000], labels[:32000]
    tweets_dev, y_dev = tweets[32000:36000], labels[32000:36000]
    tweets_test, y_test = tweets[36000:40000], labels[36000:40000]

    # convert label into numpy arrays
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    tokenizer = Tokenizer(oov_token="<UNK>")
    tokenizer.fit_on_texts(tweets_train)

    x_train = tokenizer.texts_to_matrix(tweets_train, mode="count")
    x_test = tokenizer.texts_to_matrix(tweets_test, mode="count")

    classifier = LogisticRegression(max_iter=10000, warm_start=True)
    classifier.fit(x_train, y_train)
    # print out the efficiency of the classifer model on the test set
    score = classifier.score(x_test, y_test)

    # save the classifier and tokenizer objects
    dump(classifier, 'classifier.joblib')
    dump(tokenizer, 'tokenizer.joblib')


# Training logistic regression model using TF-IDF vectorizer
# which gives importance to relative importance of word tokens
# in classifying a tweet as positive or negative
# This model uses trigrams to classify the sentiment
def train_ngram_logistic_model():
    corpus = r"train.csv"
    dataframe = pd.read_csv(corpus, header=None, usecols=[0, 5], encoding= "ISO-8859-1", names=['label', 'sentence'],)
    # shuffle the data frame as the dataset is sorted by labels
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)

    tweets = dataframe['sentence'].values
    labels = dataframe['label'].values

    # partitioning data into train, dev and test set
    tweets_train, y_train = tweets[:32000], labels[:32000]
    # tweets_dev, y_dev = tweets[32000:36000], labels[32000:36000]
    tweets_test, y_test = tweets[36000:40000], labels[36000:40000]

    # convert label into numpy arrays
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    tokenizer = Tokenizer(oov_token="<UNK>")
    # fix the vocabulary size on the train set
    tokenizer.fit_on_texts(tweets_train)

    # using a tf-idf vectorizer
    vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        strip_accents='unicode',
        analyzer='word',
        token_pattern=r'\w{1,}',
        stop_words='english',
        ngram_range=(1, 3))

    x_train = vectorizer.fit_transform(tweets_train)
    x_test = vectorizer.transform(tweets_test)

    classifier = LogisticRegression(max_iter=10000, warm_start=True)
    classifier.fit(x_train, y_train)
    score = classifier.score(x_test, y_test)
    print("Classifier Efficiency ", score)

    dump(classifier, 'classifier_ngram_tfidf.joblib')
    dump(tokenizer, 'tokenizer_ngram_tfidf.joblib')


# Finally, the last model is built using deep learning network
# where we use an LSTM to train the model as it gives importance
# to word order
def train_deep_learning_model():
    tokenizer = Tokenizer(oov_token="<UNK>")
    corpus = r"train.csv"
    dataframe = pd.read_csv(corpus, header=None, usecols=[0, 5], encoding= "ISO-8859-1", names=['label', 'sentence'],)

    # shuffle the data frame as the dataset is sorted by labels
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)

    tweets = dataframe['sentence'].values
    labels = dataframe['label'].values

    tweets_train, y_train = tweets[:32000], labels[:32000]
    tweets_dev, y_dev = tweets[32000:36000], labels[32000:36000]
    tweets_test, y_test = tweets[36000:40000], labels[36000:40000]

    tokenizer.fit_on_texts(tweets_train)

    vocab_size = tweets_train.shape[1]
    print("Vocab size =", vocab_size)

    seq_train = tokenizer.texts_to_sequences(tweets_train)
    seq_dev = tokenizer.texts_to_sequences(tweets_dev)
    seq_test = tokenizer.texts_to_sequences(tweets_test)

    maxlen = 30000
    padded_seq_train = pad_sequences(seq_train, padding='post', maxlen=maxlen)
    padded_seq_dev = pad_sequences(seq_dev, padding='post', maxlen=maxlen)
    padded_seq_test = pad_sequences(seq_test, padding='post', maxlen=maxlen)

    embedding_dim = 10

    model = Sequential(name="lstm")
    model.add(layers.Embedding(input_dim=vocab_size,
                                output_dim=embedding_dim,
                                input_length=maxlen))
    model.add(LSTM(10))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    model.summary()

    model.fit(padded_seq_train, y_train, epochs=5, verbose=True, validation_data=(padded_seq_dev, y_dev), batch_size=10)

    loss, accuracy = model.evaluate(padded_seq_test, y_test, verbose=False)
    #print('Model Accuracy and Loss :: ', accuracy, ' ', loss)

    dump(model, 'model_deep_learning.joblib')
    dump(tokenizer, 'tokenizer_deep_learning.joblib')


train_model()
train_ngram_logistic_model()
train_deep_learning_model()
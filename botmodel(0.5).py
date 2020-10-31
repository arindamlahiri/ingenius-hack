# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/********
"""





#importing required libraries
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from pathlib import Path
import string
import re
import random
import joblib
import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import contractions
from sklearn.preprocessing import LabelEncoder
import profanity_check as pck
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, Flatten
from tensorflow.keras.layers import Conv1D
from tensorflow.keras import regularizers
from tensorflow.keras.layers import MaxPooling1D
from keras.layers import Dropout, Embedding, LSTM, Bidirectional
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tensorflow import keras
from sklearn.utils import shuffle
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

#downloading the sample wordnet dataset (to be run once)
nltk.download('wordnet')



#importing dataset
df = pd.read_csv("datafinal1.csv", encoding='cp1252')
df.head()

#find the number of classes
df.label.unique()

#Encode categorical variable
le=LabelEncoder()
df['label'] = le.fit_transform(df['label'])
df.head()

#Aliases for encoded values
encoded_dict = {0:"hate", 1:"no hate"}
encoded_dict

"""# Text Preprocessing"""

lem = WordNetLemmatizer()
words = Counter()
labels = []
#splitting input into tokens
def tokenizer(x):
    tokens = x.split()
    rep = re.compile('[%s]' % re.escape(string.punctuation))
    tokens = [rep.sub('', i) for i in tokens]
    #tokens = [i for i in tokens if not i.isdigit()]
    t=[]
    for i in tokens:
      r = ''.join([x for x in i if not x.isdigit()]) 
      if len(r)>0:
        t.append(r)
    tokens=t 
    tokens = [lem.lemmatize(i.lower()) for i in tokens]
    tokens = [i.lower() for i in tokens if len(i) > 1]
    return tokens

#removing stop words
def no_stopwords(tokenizer,df,c):
    no_stop = []
    for x in df[c]:
        tokens = tokenizer(x)
        joblib.dump(tokens,'tokens.pkl')
        no_stop.append(' '.join(tokens))
    df[c] = no_stop
    return

#storing retrieved tokens
def new_words(tokenizer,df,c):
    for x in df[c]:
        tokens = tokenizer(x)   
        words.update(tokens)
    joblib.dump(words,'words.pkl')
    return

new_words(tokenizer,df,'text')
no_stopwords(tokenizer,df,'text')

#check for encoded and cleaned data
df.head()

#Encoding text data into vectors (to be sent as input to the model)
def encoder(df, c):
    ent = [x for x in df[c]]
    tokenizer = Tokenizer(num_words=50000)
    tokenizer.fit_on_texts(ent)
    joblib.dump(tokenizer,'tokenizer_t.pkl')
    encoded = tokenizer.texts_to_sequences(ent)
    word_index = tokenizer.word_index
    wordlen= len(word_index)+1
    max_length = max([len(s.split()) for s in ent])
    text = pad_sequences(encoded, maxlen=500)

    return (text, wordlen, max_length )

X,wordlen,max_length = encoder(df,'text')
X

#Converting encoded values into a dataframe and adding the labels
dfen = pd.DataFrame(X)
dfen['label'] = df["label"]
dfen.head()

#Splitting dataset into dependent and independent variables
xx = dfen.drop(columns=['label'],axis=1)
yy = dfen['label']
#one-hot encode values of dependent variable
yy = pd.get_dummies(yy).values
#Splitting dataset into test and train sets
X_train,X_test, y_train, y_test =  train_test_split(xx, yy,test_size =0.1,random_state= 42)

"""# Model"""

#define early stopping to stop the training in case the metrics do not improve
early_stopping = EarlyStopping(monitor='val_loss',patience=5)
cp = ModelCheckpoint("botmodel.h5",
                             monitor="val_loss",
                             mode="min",
                             save_best_only = True,
                             verbose=1)
rlr = ReduceLROnPlateau(monitor = 'val_loss', factor = 0.2, patience = 3, verbose = 1, min_delta = 0.0001)
total_call = [early_stopping,cp,rlr]

#Model architecture
def build_model(wordlen):
    model = Sequential()
    #model.add(LSTM(1, activation='relu'))
    model.add(Embedding(5000,300, input_length=500))
    model.add(Conv1D(filters=64, kernel_size=4, activation='relu'))
    model.add(MaxPooling1D(pool_size=8))
    model.add(Flatten())
   # model.add(LSTM(1, activation="relu", return_sequences=True))
    model.add(Dense(2, activation='sigmoid', activity_regularizer=regularizers.l2(l2=0.01)))
    
    model.compile(loss = 'binary_crossentropy',
              optimizer = 'adam',
              metrics = ['accuracy'])
    model.summary()
    return model

#building the model
model = build_model(wordlen)

#training the model
mod_sum = model.fit(X_train, y_train, epochs=500, verbose=1,
                    validation_data=(X_test, y_test), batch_size = 32, callbacks=total_call)

#Plotting training and validation accuracy and loss
plt.plot(mod_sum.history['accuracy'])
plt.plot(mod_sum.history['val_accuracy'])
plt.xlabel("epochs")
plt.ylabel('accuracy')
plt.legend(['train_accuracy', 'test_accuracy'])
plt.show()

plt.plot(mod_sum.history['loss'])
plt.plot(mod_sum.history['val_loss'])
plt.xlabel("epochs")
plt.ylabel('loss')
plt.legend(['train_loss', 'test_loss'])
plt.show()

"""# Testing"""

#importing the required library and loading files onto the workspace
from tensorflow.keras.models import load_model
model = load_model('botmodel.h5')
tok = joblib.load('tokenizer_t.pkl')
words_ = joblib.load('words.pkl')

#converting input into a dataframe
def get_text(x):
    input_text  = [x]
    df_input = pd.DataFrame(input_text,columns=['text'])
    df_input
    return df_input

#converting input into tokens
def tokenizer(x):
    tokens = x.split()
    rep = re.compile('[%s]' % re.escape(string.punctuation))
    tokens = [rep.sub('', i) for i in tokens]
    #tokens = [i for i in tokens if i.isalpha()]
    t=[]
    for i in tokens:
      r = ''.join([x for x in i if not x.isdigit()]) 
      if len(r)>0:
        t.append(r)
    tokens=t 
    tokens = [lem.lemmatize(i.lower()) for i in tokens]
    tokens = [i.lower() for i in tokens if len(i) > 1]
    return tokens

#removing stop words
def no_stop_inp(tokenizer,df,c):
    no_stop = []
    x = df[c][0]
    tokens = tokenizer(x)
    no_stop.append(' '.join(tokens))
    df[c] = no_stop
    return df

#encoding tokens retrieved from input
def inpenc(tok,df,c):
    ent = [df[c][0]]
    tokenizer = tok
    tokenizer.fit_on_texts(ent)
    encoded = tokenizer.texts_to_sequences(ent)
    text = pad_sequences(encoded, maxlen=500)
    return text

#input 
x=input()
df3 = get_text(x)
#loading files required for preprocessing
tok = joblib.load('tokenizer_t.pkl')
word = joblib.load('words.pkl')
df3 = no_stop_inp(tokenizer,df3,'text')
inp = inpenc(tok,df3,'text')
#predicting nature of the sentence
p = model.predict_classes(inp)
for i in p:
  print(encoded_dict[i])

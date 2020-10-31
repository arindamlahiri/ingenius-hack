import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
import profanity_check as pck
#import contractions
import string
import re
import json
import emoji
import nltk
import sys
#run on the first time alone :
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import demoji
demoji.download_codes()

model = load_model('botmodel(0.5).h5')
tok = joblib.load('tokenizer_t.pkl')
words = joblib.load('words.pkl')
dfem = pd.read_csv('emoji_dataset.csv')

encoded_dict = {0:'offensive', 1: 'not offensive'}
ddict=dict()

#cleaning
lem = WordNetLemmatizer()
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

def no_stop_inp(tokenizer,df,c):
    no_stop = []
    x = df[c][0]
    tokens = tokenizer(x)
    no_stop.append(' '.join(tokens))
    df[c] = no_stop
    return df

def inpenc(tok,df,c):
    ent = [df[c][0]]
    tokenizer = tok
    tokenizer.fit_on_texts(ent)
    encoded = tokenizer.texts_to_sequences(ent)
    text = pad_sequences(encoded, maxlen=500)
    return text

#input
def get_text(x):
    df_input = pd.DataFrame(x,columns=['text'])
    df_input
    return df_input

#output
x = str(sys.argv[1])
#print("input = ",  x)
#x = [input()]
ddict=demoji.findall(x)
res = list(ddict.values())
if(len(res)!=0):
    for em in res:
        if em in dfem.values:
            flag = 0
            break
        else:
            flag = 1
    if(flag==0):
        print("offensive")
        exit()
    
for k in x:
    if(emoji.UNICODE_EMOJI.get(k)!=None):
        x=x.replace(k,'')
if(len(x)==0):
    print("not offensive")
else:
    for i in pck.predict([x]):
      if (i==1):
        print("offensive")
        exit()
      else:
        df3 = get_text([x])
        tok = joblib.load('tokenizer_t.pkl')
        word = joblib.load('words.pkl')
        df3 = no_stop_inp(tokenizer,df3,'text')
        inp = inpenc(tok,df3,'text')
        p = model.predict_classes(inp)
        for i in p:
          print(encoded_dict[i])


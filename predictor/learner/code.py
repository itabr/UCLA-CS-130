
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import numpy as np
import re
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import svm

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier



from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.naive_bayes import GaussianNB

import nltk
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer

from sklearn.model_selection import GridSearchCV



from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
# In[2]:


t = pd.read_csv("./reports/data.csv")


# In[3]:


__type = "math"#sys.argv[1]
t[__type] =  t["labels"].str.contains(__type)
t[__type] = pd.to_numeric(t[__type], downcast="signed")


# In[4]:


feature = "problem-statement"
output = t[[__type,feature]]
output = output.dropna()

output[__type] = output[__type].astype(int)

df = pd.DataFrame(columns=[__type, feature])

a = output.loc[output[__type] == 1.0]
b = output.loc[output[__type] == 0.0]
b = b.sample(n=len(a), random_state = 42)


# In[5]:


output = a.append(b)


# In[6]:


stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words="english",analyzer = 'word')

l = output[feature].tolist()
res = []
regex = re.compile('^a-zA-Z0-9')
def clean_s(input_str):
    return regex.sub(' ', input_str)

for i in range(len(l)):
    try:
        res.append(clean_s(l[i]))
    except:
        res.append("")

X = vectorizer.fit_transform(res)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,output[__type], test_size=0.2,random_state=42)




max_features = 5000
maxlen = 400
batch_size = 32
embedding_dims = 50
filters = 250
kernel_size = 3
hidden_dims = 250
epochs = 2

X_train = sequence.pad_sequences(X_train.toarray(), maxlen=maxlen)
X_test = sequence.pad_sequences(X_test.toarray(), maxlen=maxlen)

model = Sequential()

# we start off with an efficient embedding layer which maps
# our vocab indices into embedding_dims dimensions
model.add(Embedding(max_features,
                    embedding_dims,
                    input_length=maxlen))
model.add(Dropout(0.2))

# we add a Convolution1D, which will learn filters
# word group filters of size filter_length:
model.add(Conv1D(filters,
                 kernel_size,
                 padding='valid',
                 activation='relu',
                 strides=1))
# we use max pooling:
model.add(GlobalMaxPooling1D())

# We add a vanilla hidden layer:
model.add(Dense(hidden_dims))
model.add(Dropout(0.2))
model.add(Activation('relu'))

# We project onto a single unit output layer, and squash it with a sigmoid:
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
validation_data=(X_test, y_test))


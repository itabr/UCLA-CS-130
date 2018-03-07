
# coding: utf-8

# In[15]:

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

import theano
import theano.tensor as T

import lasagne
# In[16]:


t = pd.read_csv("./data.csv")


# In[17]:


__type = sys.argv[1]
t[__type] =  t["labels"].str.contains(__type)
t[__type] = pd.to_numeric(t[__type], downcast="signed")


# In[18]:

feature = "problem-statement"
output = t[[__type,feature]]
output = output.dropna()

output[__type] = output[__type].astype(int)

df = pd.DataFrame(columns=[__type, feature])

a = output.loc[output[__type] == 1.0]
b = output.loc[output[__type] == 0.0]
b = b.sample(n=len(a), random_state = 42)


# In[19]:


output = a.append(b)


# In[20]:

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



# In[21]:

#model = linear_model.RidgeCV(alphas = [0.1, 1.0, 10])
#parameters = {}
#model = linear_model.Lasso(alpha=0.0001)
#model = linear_model.SGDClassifier(loss = 'hinge', penalty='l2')
#parameters = {}
#model = GaussianNB()

### -->logistic regression
#model = linear_model.LogisticRegression(class_weight= 'balanced')
#parameters = {'solver':('newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'), 'C':[0.1, 1, 10,100], 'max_iter': [100,1000]}

### -> logistic regression
#model = LinearSVC()
model = MLPClassifier(solver='lbfgs',  hidden_layer_sizes= (100,100,100), random_state=1)
parameters={}
#parameters = {'C':[ 0.1, 1, 10,100]}
### --> randomforest
#model = RandomForestClassifier(class_weight = 'balanced')
#parameters={}
### --> random forest


#model = AdaBoostClassifier(n_estimators=100)
#parameters= {'n_estimators': (10,100,1000)}
#### ---> SVC
#model = svm.SVC()
#parameters = {'kernel':('linear', 'rbf', 'poly', 'sigmoid'), 'C':[ 1, 10]}
### ---> SVC 
clf = GridSearchCV(model, parameters)

# In[22]:

X_train, X_test, y_train, y_test = train_test_split(X,output[__type], test_size=0.2,random_state=42)

# for neural network only

# ------>end 

clf.fit(X_train, y_train)
#print sorted(clf.cv_results_.keys())

y_pred = clf.predict(X_test)
y_pred = [round(value) for value in y_pred]

print __type
print classification_report(y_test, y_pred)


# In[23]:



# In[24]:


#output[["label","problem-statement"]].to_csv("./res.txt",index=False,header=False)


# In[25]:

print "number of positive samples " + str(len(a))
print

# In[26]:




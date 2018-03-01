
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

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier


from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.naive_bayes import GaussianNB
# In[16]:


t = pd.read_csv("./test.csv")


# In[17]:


__type = sys.argv[1]
t[__type] =  t["labels"].str.contains(__type)
t[__type] = pd.to_numeric(t[__type], downcast="signed")


# In[18]:

feature = "output-spec"
output = t[[__type,feature]]
output = output.fillna(0)
output[__type] = output[__type].astype(int)

df = pd.DataFrame(columns=[__type, feature])

a = output.loc[output[__type] == 1.0]
b = output.loc[output[__type] == 0.0]
b = b.sample(n=len(a))


# In[19]:


output = a.append(b)


# In[20]:


vectorizer = TfidfVectorizer(stop_words="english")
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
#model = linear_model.Lasso(alpha=0.0001)
#model = linear_model.SGDClassifier(loss = 'hinge', penalty='l2')
#model = GaussianNB()
model = linear_model.LogisticRegression(solver='sag')
#model = LinearSVC()
#model = MLPClassifier(solver='lbfgs',  hidden_layer_sizes= (200,200,200,200,200,200), random_state=1)
#model = RandomForestClassifier()
#model = AdaBoostClassifier(n_estimators=100)


# In[22]:

X_train, X_test, y_train, y_test = train_test_split(X,output[__type], test_size=0.1,random_state=42)

# for neural network only

# ------>end 

model.fit(X_train,y_train)
y_pred = model.predict(X_test)
y_pred = [round(i) for i in y_pred]

print __type
print classification_report(y_test, y_pred)
accuracy =  1-sum(y_pred != y_test)*1.0/len(y_pred)
print accuracy

# In[23]:



# In[24]:


#output[["label","problem-statement"]].to_csv("./res.txt",index=False,header=False)


# In[25]:

print "number of positive samples " + str(len(a))
print

# In[26]:




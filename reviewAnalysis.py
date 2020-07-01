#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import numpy as np


# In[3]:


df = pd.read_csv('IMDB Dataset.csv')
df.head()
df.shape


# In[4]:


df.head()


# In[5]:


reviews_train = []
for i in range(50000):
    reviews_train.append(df['review'][i])


# In[6]:


reviews_train[0]


# In[7]:


import re

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
    
    return reviews

reviews_train_clean = preprocess_reviews(reviews_train)


# In[8]:


reviews_train_clean[0]


# In[9]:


from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(binary=True)
cv.fit(reviews_train_clean)
X = cv.transform(reviews_train_clean)


# In[10]:


target = []
for i in range(50000):
    if(df['sentiment'][i] == 'positive'):
        target.append(1)
    else:
        target.append(0)


# In[11]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, target, train_size = 0.75)


# In[12]:


for c in [0.01, 0.05, 0.25, 0.5, 1]:
    
    lr = LogisticRegression(C=c)
    lr.fit(X_train, y_train)
    print ("Accuracy for C=%s: %s" 
           % (c, accuracy_score(y_val, lr.predict(X_val))))


# In[13]:


final_model = LogisticRegression(C=0.05)
final_model.fit(X, target)


# In[20]:


prediction = final_model.predict(X_val)


# In[21]:


score = final_model.score(X_val, y_val)
print(score)


# In[26]:


word = "a really  bad movie"
test = cv.transform([word])


# In[46]:


pred = final_model.predict(test)
pred[0]


# In[44]:


import pickle


# In[45]:


saved_model = pickle.dumps(final_model) 


# In[47]:

import joblib

filename = 'vectorizer'
fileName = 'review_analyser'
joblib.dump(final_model, fileName)
joblib.dump(cv,filename)



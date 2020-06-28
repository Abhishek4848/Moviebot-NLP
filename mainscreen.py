#!/usr/bin/env python
# coding: utf-8

# In[1]:
#TODO is mainscreen.py required?

import pandas as pd
import moviereccomendertest
import joblib
import warnings
warnings.filterwarnings("ignore")
import movie_reccomendation_genre
from textblob import TextBlob
import chatgui
def updateids():
    try:
        userids['userid'] = ids
        userids.to_csv('user_ids.csv',index = False)
    except:
        id_s = pd.DataFrame(columns=['userid'])
        id_s['userid'] = ids
        id_s.to_csv('user_ids.csv',index = False)
def mainscreen():
    print("1. LOGIN")
    print("2. SIGN-UP")
    print("3. EXIT")
    choice = (input("enter choice:"))

    if(choice == '1'):
        login()
    elif(choice == '2'):
        signup()
        updateids()
        user_data.to_csv('user_data.csv',index=False)
    elif(choice == '3'):
        exit()
    else:
        print("enter valid option")


# In[2]:


try:
    user_data = pd.read_csv('user_data.csv')
except:
    user_data = pd.DataFrame(columns=['user-id','user-name'])


# In[3]:


try:
    userids = pd.read_csv('user_ids.csv')
    ids = list(set(list(userids['userid'])))
except:
    userids = pd.read_csv('ratings.csv')
    ids = list(set(list(userids['userId'])))


# In[4]:


def signup():
    temp_data = []
    uname = input("enter user name :")
    uid = max(ids)+1
    ids.append(uid)
    temp_data.append(uid)
    temp_data.append(uname)
    i = user_data.shape[0]
    user_data.loc[i] = temp_data
    print("signup succesful ... added user to the database")
    print("use your user id:",uid," for logging in")
    mainscreen()


# In[5]:


user_data


# In[6]:


def login():
    logid = list(user_data['user-id'])
    e_id = int(input("enter user id:"))
    if(e_id in logid):
        n = logid.index(e_id)
        pushid(e_id)
        name = user_data.at[n,'user-name']
        print("welcome"+" "+name)
        print("starting chatbot...")
        chatgui.movie_chatbot()
            
    else:
        print("user not found")


# In[7]:


def pushid(eid):
    f = open("pushid.txt",'w+')
    f.write(str(eid))


# In[8]:


def getreviewd(review):
    l = []
    l.append(review)
    t = preprocess_reviews(l)
    review = t[0]
    rating =  getrating(t[0])

    cv = joblib.load('vectorizer')
    test = cv.transform([review])
    model_from_picle = joblib.load('review_analyser')
    pred = model_from_picle.predict(test)
    if(pred[0] == 1):
        print("Thank you for positive review we will consider this while reccomending you movies next time")
    elif(pred[0] == 0):
        print("Negative review detected , we will consider this while reccomending you movies next time")
    print("your predicted rating according to review : ", rating)
    return rating


# In[9]:


import re

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
    
    return reviews


# In[10]:


def getrating(t):
    blob = TextBlob(t)
    old = blob.sentiment[0]
    new = float(int((old + 1) * 2.999999999999))
    return new 


# In[11]:


def movieIdFinder(movie):
    mid = -1
    movie_titles_genre = pd.read_csv("movies.csv")
    l1 = list(movie_titles_genre['title'])
    l2 = list(movie_titles_genre['movieId'])
    for i in range(len(l1)):
        if(movie == l1[i]):
            mid = l2[i]
            break
    return mid       


# In[12]:


def tableupdater(uid,mid,rating):
    l = []
    l.append(uid)
    l.append(mid)
    l.append(rating)
    l.append('NAN')
    df = pd.read_csv('ratings.csv')
    ind = df.shape[0]
    df.loc[ind] = l
    df.to_csv('ratings.csv',index_label=False)


# In[14]:


mainscreen()


# 

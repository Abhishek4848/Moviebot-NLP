#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import pandas as pd
import moviereccomendertest
import joblib
import movie_reccomendation_genre
from textblob import TextBlob
#import chatgui
def updateids():
    try:
        userids['userid'] = ids
        userids.to_csv('user_ids.csv',index = False)
    except:
        id_s = pd.DataFrame(columns=['userid'])
        id_s['userid'] = ids
        id_s.to_csv('user_ids.csv',index = False)
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

import tkinter
from tkinter import *

def widget():
    base = Tk()
    base.title("Movie Recommender System")
    base.geometry("400x500")
    base.resizable(width=FALSE, height=FALSE)
    return base
user_name = ''
user_id = 0
def entry(error=''):
    enter = widget()
    error_label = Label(enter,text="")
    welcome = Label(enter, text = 'Wellcome!!',font = ('Arial',14,'bold')).place(x=150, y=100)
    if error != '':
        action,msg = error.split()
        if msg == '!uid':
            error_msg = f"{action} failed, User Id not found"
        elif msg == 'usr':
            error_msg = f"{action} failed, User Name exsits"
        else: error_msg = "Unknown Error, Please try again"
        error_label = Label(enter,text = error_msg, font = ('Arial',10,'italic')).place(x=100, y=250)
    
    def LogIn():
        enter.destroy()
        Login = widget()
        
        def Log():
            logid = list(user_data['user-id'])
            try:
                global user_id, user_name
                user_id = int(userId.get())
            except:
                pass
            if user_id in logid:
                n = logid.index(user_id)
                user_name = user_data.at[n,'user-name']
                Login.destroy()
            else:
                #userid not found
                Login.destroy()
                entry(error = 'LogIn !uid')

        userIdLabel = Label(Login, text = "User Id", font='Arial').place(x = 170, y = 100)
        userId = StringVar()
        userIdEntry = Entry(Login, textvariable=userId, width = 25).place(x = 125, y = 140)
        login = Button(Login, text = 'Login',command = Log).place(x=175, y = 170)
        Login.mainloop()
       
        
    
    def SignUp():
        enter.destroy()
        Signup = widget()
        
        def Sign():
            usrs = list(user_data['user-name'])
            global user_name, user_id
            user_name = username.get()
            if user_name in usrs:
                #user name exists
                Signup.destroy()
                entry(error = 'SignUp usr')
            else:
                temp_data = []
                uid = max(ids)+1
                user_id = uid
                ids.append(uid)
                temp_data.append(uid)
                temp_data.append(user_name)
                i = user_data.shape[0]
                user_data.loc[i] = temp_data
                updateids()
                user_data.to_csv('user_data.csv',index=False)
                Signup.destroy()
            
        usernameLabel = Label(Signup, text = "Enter User Name", font='Arial').place(x = 120, y = 100)
        username = StringVar()
        usernameEntry = Entry(Signup, textvariable=username, width = 25).place(x = 120, y = 140)
        signup = Button(Signup, text = 'Sign In',command = Sign).place(x=165, y = 170)
        Signup.mainloop()
        
        
    signup = Button(enter, text= 'Sign Up',font=('verdana',12,'italic'), width = 20, bg="#32de97", command = SignUp)
    signup.place(x=100, y=150)
    
    login = Button(enter, text= 'Login',font=('verdana',12,'italic'), width = 20, bg="#32de97", command = LogIn)
    login.place(x=100, y=200)
    enter.mainloop()
    return user_name,user_id
# In[7]:


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
    
    return rating, pred[0]


# In[8]:


import re

REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]
    
    return reviews


# In[9]:


def getrating(t):
    blob = TextBlob(t)
    old = blob.sentiment[0]
    new = ((1+old)/2)*5
    return new 


# In[10]:


def movieIdFinder(movie):
    mid = -1
    mov = ''
    movie_titles_genre = pd.read_csv("movies.csv")
    l1 = list(movie_titles_genre['title'])
    l2 = list(movie_titles_genre['movieId'])
    for i in range(len(l1)):
        if(movie == l1[i]):
            mid = l2[i]
            mov = l1[i]
            break
    return mid,mov      


# In[11]:


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

print(movieIdFinder('avengers'))
# In[12]:




# In[13]:




# 

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import movie_reccomendation_genre
import random
import moviereccomendertest

# In[2]:


df = pd.read_csv('ratings.csv')


# In[3]:


def getmovieid(uid):
    df = pd.read_csv('ratings.csv')
    mid = []
    rating = []
    final = []
    for i in range(len(df['userId'])):
        if(uid == df['userId'][i]):
            mid.append(df['movieId'][i])
            rating.append(df['rating'][i])
    if(rating == []):
        #print("sorry could not get movies based on review history since you haven't reviewed any movie, getting movies that you might like")
        final = random.sample(list(df['movieId']),1)
    else:
        maxr = rating.index(max(rating))
        final.append(mid[maxr])
    return rating, final


# In[4]:


df2 = pd.read_csv('movies.csv')

def getgenre(t):
    if(t == []):
        exit()
    else:
        for i in range(len(df2['movieId'])):
            if(t[0] == df2['movieId'][i]):
                genre_str = df2['title'][i]
                #l = genre_str.split('|')
                #final_genre = random.sample(l,1)
                #final_genre = list(genre_str)
        return genre_str

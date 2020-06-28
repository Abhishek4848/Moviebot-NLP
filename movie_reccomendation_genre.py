#!/usr/bin/env python
# coding: utf-8

# In[2]:

from imdb import IMDb
import pandas as pd
import random


# In[3]:


df = pd.read_csv("movies.csv")


# In[4]:


def searchbygenre(search):
    movielist = []
    dftolist = df.values.tolist()
    for i in range (len(dftolist)):
            if search.lower() in dftolist[i][2].lower():
                movielist.append(dftolist[i][1])
        
    return movielist


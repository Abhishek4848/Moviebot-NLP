#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:
def cosine_recommendations(title):
    movies = pd.read_csv('movies.csv')
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(movies['genres'])

    from sklearn.metrics.pairwise import linear_kernel
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    titles = movies['title']
    indices = pd.Series(movies.index, index=movies['title'])
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    l = list(titles.iloc[movie_indices].head(5))
    return l


def failsafe(title):
    df = pd.read_csv('movies.csv')
    l = list(df['title'])
    if title not in l:
        flag = 'Fail'
        return flag
    else:
        flag = 'pass'
        return flag

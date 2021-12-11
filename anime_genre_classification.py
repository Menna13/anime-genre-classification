# -*- coding: utf-8 -*-
"""Anime Genre Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K09TskXUW2iQIqP1JyNmCwKHDi9d0wB7
"""

pip install Unidecode

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from unidecode import unidecode
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

nltk.download('stopwords')
nltk.download('punkt')

import os
import urllib.request
import matplotlib.pyplot as plt
from scipy import spatial
from sklearn.manifold import TSNE
import numpy as np



"""### Loading Data"""

#importing anime dataset from our github repository
url = 'https://raw.githubusercontent.com/Menna13/anime-genre-classification/main/animes.csv'
anime_df = pd.read_csv(url)

#Mohamed's genre extraction code
data = anime_df[['title', 'synopsis', 'genre']]
#delete all rows that has null genre
#TODO: get how many null values dropped to include in paper
data = data.dropna(subset=['genre'], how='all')
data = data.dropna(subset=['synopsis'], how='all')
#print(df['genre'])
genres = set()
for genre in data['genre']:
    #split genre by ',' and igonre first and last characters which are (' and ')
    s = genre[1:-1].split(',')
    for i in s:
        stripped = i.replace('\'', '').replace(' ', '')
        genres.add(stripped)
print(len(genres), genres)
# Total of 43 genre

"""### Preprocess Synopsis

"""

# pre-processing the synopsis 

anime_corpus = data['synopsis']
anime_corpus = ' '.join(anime_corpus)

def pre_process(anime_corpus):
    # convert input corpus to lower case.
    anime_corpus = anime_corpus.lower()
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)
    # remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input corpus in word tokens.
    anime_corpus = " ".join([i for i in word_tokenize(anime_corpus) if i not in stopset])
    # remove non-ascii characters
    anime_corpus = unidecode(anime_corpus)
    return anime_corpus

pre_process(anime_corpus)

#Next Step, add GloVe embeddings and if possible try other kinds of embeddings such as tf-idf and word2vec and compare their results with GloVe's

"""### Embeddings"""

urllib.request.urlretrieve('https://nlp.stanford.edu/data/glove.6B.zip','glove.6B.zip')

!unzip "/content/glove.6B.zip" -d "/content/"

def extract_embeddings(path):
  emmbed_dict = {}
  with open(path,'r') as f:
    for word_vector in f:
      v = word_vector.split()
      word = v[0]
      vector = np.asarray(v[1:], 'float32')
      emmbed_dict[word]= vector 
  return emmbed_dict

emmbed_dict = extract_embeddings('/content/glove.6B.200d.txt')
print(emmbed_dict)

#eculidian distance is given to the sorting function to work as a sorting key. eculidian distance function finds the distance between two 1-D arrays
def find_similar_word(word_vector, top_k): 
  nearest = sorted(emmbed_dict.keys(), key = lambda word: spatial.distance.euclidean(emmbed_dict[word],word_vector))
  return nearest[:top_k]

find_similar_word(emmbed_dict['anime'], 10)



"""
 Question: can we consider all synopsis together as our corpus?

- possibly using a lemmatizer but after a discussion with Alvin, it's possible it won't help much if LSTM model is character level

- QUESTION: what label to give to an anime ? ? ? ? ? ? ? ? ? Answer: Multi label classification is possible 

- for embeddings, possibly download one trained on a large netword and then fine tune it using your specific data

- multi-label classification can be acheived using Vowpal Wabbit: https://towardsdatascience.com/multi-label-classification-using-vowpal-wabbit-from-why-to-how-c1451ca0ded5
 https://www.pyimagesearch.com/2018/05/07/multi-label-classification-with-keras/

- Possible different Word Embedding model, TF-IDF and Smooth Inverse Frequency (SIF): https://monkeylearn.com/blog/what-is-tf-idf/
 https://intellica-ai.medium.com/comparison-of-different-word-embeddings-on-text-similarity-a-use-case-in-nlp-e83e08469c1c
 https://towardsdatascience.com/creating-word-embeddings-coding-the-word2vec-algorithm-in-python-using-deep-learning-b337d0ba17a8
 https://medium.com/analytics-vidhya/text-classification-using-word-embeddings-and-deep-learning-in-python-classifying-tweets-from-6fe644fcfc81
 https://analyticsindiamag.com/hands-on-guide-to-word-embeddings-using-glove/
"""
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from sklearn.manifold import TSNE
from gensim.models import Word2Vec,KeyedVectors
from sklearn import cluster,metrics
import pickle
from sklearn.neighbors import NearestNeighbors
import textwrap
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
import nltk
import gensim.downloader as api


modelg = api.load("word2vec-google-news-300")

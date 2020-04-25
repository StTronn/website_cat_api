import numpy as np
from sklearn.neighbors import NearestNeighbors
from gensim.models import Word2Vec,KeyedVectors
import textwrap
import gensim.downloader as api
from helper import load_kmeans,sent_vectorizer
from get_url import get_content
from sklearn.neighbors import NearestNeighbors

EMBEDDING_FILE = 'GoogleNews-vectors-negative300.bin.gz'
modelg= KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True,limit=100000)
kmeans=load_kmeans()
#content = get_content(url)


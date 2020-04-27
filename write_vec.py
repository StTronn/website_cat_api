import pickle
from gensim.models import Word2Vec,KeyedVectors
import pandas as pd

EMBEDDING_FILE = './GoogleNews-vectors-negative300.bin.gz'
modelg= KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True,limit=40000)

def store_object(obj,filename):
  with open(filename,'wb') as obj_file:
    pickle.dump(obj,obj_file)

store_object(modelg,'modelg')



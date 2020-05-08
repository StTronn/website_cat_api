import pandas as pd
import pickle
import numpy as np
from gensim.models import Word2Vec,KeyedVectors
from sklearn import cluster,metrics
import gensim.downloader as api
from urllib.parse import urlparse
import scipy
from server import y,z,centroid_no,modelg,X

def load_obj(filename):
  with open(filename,'rb') as obj_file:
    obj = pickle.load(obj_file)
    return obj




def sent_vectorizer(sent, modelg):
    sent_vec =[]
    numw = 0
    for w in sent:
        try:
            if numw == 0:
                sent_vec = modelg[w]
            else:
                sent_vec = np.add(sent_vec, modelg[w])
            numw+=1
        except:
            pass
    return np.asarray(sent_vec) / numw

def create_vector(sentences):
  X=[]
  for sentence in sentences:
     X.append(sent_vectorizer(sentence, modelg))
  return X

def get_centroid_websites(num=-1):
  if num==-1:
    return X,y,z,centroid_no
  else:
    new_X=[]
    new_Y=[]
    new_Z=[]
    new_C=[]
    for i in range (len(y)):
      if(centroid_no[i]==num):
        new_X.append(X[i])
        new_Y.append(y[i])
        new_Z.append(z[i])
        new_C.append(c[i])
    return new_X,new_Y,new_Z,new_C

def search_by_query(query,centroid_no=-1,no_of_results=20):
    vectors,urls,ranks,centroid_num=get_centroid_websites(centroid_no)
    query_vector=sent_vectorizer(query,modelg)
    similarity=[]
    for x in vectors:
      try:
          dist=scipy.spatial.distance.cosine(query_vector,x)
          similarity.append(dist)
      except:
        pass
    top_idx = np.argsort(similarity)[0:no_of_results]
    top_url= [[urls[i],ranks[i],similarity[i]] for i in top_idx]
    rank_list=[(0.5*t[1])+(0.5*t[2]) for t in top_url]
    top_rank_idx = np.argsort(rank_list)
    final_rank=[top_url[i][0] for i in top_rank_idx]
    return final_rank


def search_by_domain(query_domain,centroid_no=-1):
      X,y,z,c=get_centroid_websites(centroid_no)

      domains=[]
      for url in y:
        d=urlparse(url).netloc
        for word in query_domain:
          if word in d:
            domains.append(url)
      return domains







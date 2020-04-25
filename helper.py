#kmeans object is kmeans_file
#cluster is stored in sites_50_google.cluster
#for the function to work we will require the google model also
import pickle
import numpy as np

def read_cluster(filename=''):
  with open('sites_50_google.cluster', 'rb') as cluster_file:
    cluster = pickle.load(cluster_file)
    return cluster

def load_kmeans():
  with open('kmeans_file', 'rb') as kmeans_file:
    kmeans = pickle.load(kmeans_file)
    return kmeans

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

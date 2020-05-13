#kmeans object is kmeans_file
#cluster is stored in sites_50_google.cluster
#for the function to work we will require the google model also
import pickle
import numpy as np
import sqlite3

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


def read_csv(df):
    df=df.head(50000)
    y=df.url.tolist()
    z=df['rank'].tolist()
    c=df.centroid_no.tolist()
    return y,z,c

def get_cluster_sites(cluster_no=-1):
    conn = sqlite3.connect("server/database/web.db")
    cur = conn.cursor()
    urls=[]
    ranks=[]
    ret=[]
    if cluster_no==-1:
        cur.execute("SELECT * FROM data LIMIT 100000")
    else:
        cur.execute("SELECT * FROM data where cluster_no=?",(str(cluster_no)))
    rows = cur.fetchall()
    print("data fetched..")
    print("calculating..")
    for row in rows:
        o={}
        o['url']=row[1]
        o['rank']=row[5]
        ret.append(o)
    return ret[:20]

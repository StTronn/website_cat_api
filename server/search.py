import pandas as pd
import pickle
import sys
import numpy as np
from gensim.models import Word2Vec,KeyedVectors
from sklearn import cluster,metrics
import gensim.downloader as api
from urllib.parse import urlparse
import scipy
from server.initialize import sent_vectorizer
import sqlite3

def get_cluster_websites(query_vector,cluster_num=-1,):
  conn = sqlite3.connect("server/database/web.db")
  cur = conn.cursor()
  urls=[]
  ranks=[]
  similarity=[]
  if cluster_num==-1:
      cur.execute("SELECT * FROM data LIMIT 100000")
      print("data fetched..")
      rows = cur.fetchall()
      print("calculating..")
      for row in rows:
        urls.append(row[1])
        ranks.append(row[5])
        v=[float(x) for x in row[4].split()]
        try:
         similarity.append(scipy.spatial.distance.cosine(query_vector,v))
        except:
          pass
      return urls,ranks,similarity
  else:
      cur.execute("SELECT * FROM data where cluster_no=?",(str(cluster_num)))
      rows = cur.fetchall()
      print("data fetched..")
      print("calculating..")
      for row in rows:
        urls.append(row[1])
        ranks.append(row[5])
        v=[float(x) for x in row[4].split()]
        try:
          similarity.append(scipy.spatial.distance.cosine(query_vector,v))
        except:
          pass
      return urls,ranks,similarity


def search_by_query(query,cluster_no=-1,no_of_results=20):
    query_vector=sent_vectorizer(query)
    urls,ranks,similarity=get_cluster_websites(query_vector,cluster_no)

    print("fetching top sites...")
    rank_list=[]
    top_idx = np.argsort(similarity)[0:no_of_results]
    top_urls=[{"url":urls[i],"rank":ranks[i],"similarity":similarity[i]} for i in top_idx]
    for i in top_idx:
      if(ranks[i]!=None):
        rank_list.append((0.5*similarity[i])+(0.5*ranks[i]))
      else:
        rank_list.append(sys.maxsize)
    final_idx=np.argsort(rank_list)
    final_rank=[{'url':top_urls[i]["url"],'rank':top_urls[i]["rank"]} for i in final_idx]
    return final_rank




def search_by_domain(query_domain,no_of_results=50):
      conn = sqlite3.connect("server/database/web.db")
      cur = conn.cursor()
      cur.execute("SELECT * FROM data")
      rows = cur.fetchall()
      urls=[]
      ranks=[]
      domains=[]
      for i in range(len(rows)):
        d=urlparse(rows[i][1]).netloc
        for word in query_domain:
          if word in d:
            domains.append({"url":rows[i][1],"rank":rows[i][5]})
      return domains[0:no_of_results]

print(search_by_query(["school"]))

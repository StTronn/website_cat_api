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

def get_all_vectors(cluster=None):
  """ return  dictionary consist list of urls, and embeddings of given cluster,
      in case of None it return vectors of all cluster """

  conn = sqlite3.connect("./server/database/web.db")
  cur=conn.cursor()
  query = "SELECT  "
  for i in range(50):
    query += 'emb_d' + str(i)
    if(i != 49): query += ', '
  query += ' FROM global_data '

  if(cluster>-1 and cluster<100): query += 'WHERE cluster='+str(cluster)

  try:
    cursor = cur.execute(query)
    for row in cursor:
      yield list(row[0:])
  except sqlite3.Error as error:
     print(error)

def search_by_query(query,cluster_no=-1,no_of_results=20):
    print(cluster_no)
    conn = sqlite3.connect("./server/database/web.db")
    cur = conn.cursor()
    query_vector=sent_vectorizer(query)
    urls=[]
    ranks=[]
    similarity=[]
    rows=[]
    if cluster_no<0 or cluster_no>100:
      cur.execute("SELECT url,rank_d30 FROM global_data LIMIT 100000")
    else:
      cur.execute("SELECT url,rank_d30 FROM global_data where cluster=?",(str(cluster_no),))
    
    try:
      
      for row,v in zip(cur,get_all_vectors(cluster_no)):
        urls.append(row[0])
        ranks.append(row[1])
        similarity.append(scipy.spatial.distance.cosine(query_vector,v))
       
    except :
          pass
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
    conn = sqlite3.connect("./server/database/web.db")
    cur = conn.cursor()
    cur.execute("SELECT url,rank_d30 FROM global_data")
    rows = cur.fetchall()
    domains=[]
    for i in range(len(rows)):
        d=urlparse(rows[i][0]).netloc
        for word in query_domain:
            if word in d:
                domains.append({"url":rows[i][0],"rank":rows[i][1]})
    return domains[0:no_of_results]

def get_cluster_websites(cluster_no=-1):
  conn = sqlite3.connect("./server/database/web.db")
  cur = conn.cursor()
  ret=[]
  rows=[]
  if cluster_no <0 or cluster_no >100:
      cur.execute("SELECT url,rank_d1,rank_d2 FROM global_data")
  else :
    cur.execute("SELECT url,rank_d1,rank_d2 FROM global_data where cluster=?",(str(cluster_no),))
  rows = cur.fetchmany(20)
  print (rows)
  for row in rows:
      result_dict={}
      result_dict['url']=row[0]
      result_dict['rank']=row[1]
      if row[2]==None or row[1]==None:
          result_dict['change']=0
      else:
          result_dict['change']=row[2]-row[1]
      ret.append(result_dict)
  return ret

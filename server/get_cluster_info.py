import json
import sqlite3

DB_URL="./server/database/web.db"

def getRank(clusterNo):
   rank_list=[]
   con = sqlite3.connect(DB_URL)
   cur = con.cursor()
   cur.execute("select c"+clusterNo+" from RANK")
   con.commit()
   rows = cur.fetchall()
   for row in rows:
       rank_list.append(row[0])
   return rank_list

def getkeywords(clusterNo):
   keyword_list=[]
   con = sqlite3.connect(DB_URL)
   cur = con.cursor()
   cur.execute("select c"+clusterNo+" from KEYWORDS")
   con.commit()
   rows = cur.fetchall()
   for row in rows:
       keyword_list.append(row[0])
   return keyword_list

def getSize(clusterNo):
   size_list=[]
   con = sqlite3.connect(DB_URL)
   cur = con.cursor()
   cur.execute("select c"+str(clusterNo)+" from SIZE")
   con.commit()
   rows = cur.fetchall()
   for row in rows:
       size_list.append(row[0])
   return size_list

def getCluster(clusterNo):
   cluster_object = {"rank":[],"size":[],"keywords":[]}
   rank_list=[]
   size_list=[]
   keywords_list=[]
   clusterNo=str(clusterNo)
   rank_list=getRank(clusterNo)
   size_list=getSize(clusterNo)
   keywords_list=getkeywords(clusterNo)
   cluster_object['rank']=rank_list
   cluster_object['size']=size_list
   cluster_object['keywords']=keywords_list
   return cluster_object

def getInfo():
   all_clusters={}
   for i in range(0,100):
      all_clusters[i]=getCluster(i)
   return all_clusters


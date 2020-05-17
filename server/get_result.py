from sklearn.neighbors import NearestNeighbors
from datetime import date
from datetime import timedelta 
import sqlite3
from server.initialize import kmeans,modelg,sent_vectorizer
from server.get_url import preprocess
from scrapper import get_text_content
import json
#need to bring exact correct kmeans and wb.db accoringly and trends.db accordingly

def keyWordsOfCluster(clusterNo):
  keywords=[]
  conn = sqlite3.connect('server/database/web.db')
  #need to change day to date_p in next line remember
  # remeber to change query for that day not day before
  cursor = conn.execute("SELECT c"+str(clusterNo)+" from KEYWORDS where date_p='"+str(date.today() - timedelta(days = 15))+"'")
  for row in cursor:
    keywords=(row[0].split())
  conn.close()
  return keywords
  # return []

def getIndexOfNearVectors(urlVector,vectors):
  try:

    neigh = NearestNeighbors(2, 0.4)
    neigh.fit(vectors)
    # change this near vector from 5 to 10
    index = neigh.kneighbors([urlVector], 10, return_distance=False)
    return index
  except Exception as e:
    print("getIndexOfNearVectors",e)
    return e

def sToVec(vectorstr):
  vectors=[]
  lst = [float(x) for x in vectorstr.split()]
  return lst

def getAllVecorsOfCluster(cluster=None):
  """ return  dictionary consist list of urls, and embeddings of given cluster, 
      in case of None it return vectors of all cluster """

  query = "SELECT url, "
  for i in range(50):
    query += 'emb_d' + str(i)
    if(i != 49): query += ', '
  query += ' FROM global_data '

  if(cluster is not None): query += 'WHERE cluster='+str(cluster)

  try:
    
    conn = sqlite3.connect("server/database/web.db") 
    cur = conn.cursor()
    cursor = cur.execute(query)
    print("embedding of all urls from database done")
    urls, embedding = [], []
    
    for row in cursor:
      urls.append(row[0])
      embedding.append(row[1:])
    print("Finally all url vectors preapred (X)")
    return dict({'vectors':embedding,'urls':urls})

  except sqlite3.Error as error:
    print("getAllVecorsOfCluster Error",error)

  finally:
    if (conn): conn.close()

"""
def getAllVecorsOfCluster(clusterno):
  urlsVectors=[]
  urls=[]
  # Need to fetch url,vector from db and again convet that vector str to vector
  
  conn = sqlite3.connect('server/database/web.db')
  cursor = conn.execute("SELECT url,embedding from data where cluster_no="+str(clusterno))
  print("embedding of all urls in this cluster done")
  for row in cursor:
    # keywords=(row[0].split())
    urls.append(row[0])
   # print("url",row[0])
    urlsVectors.append(sToVec(row[1]))
   # print("url vector appended")
  print("X prepared")
  conn.close()
  #
  #    
  return dict({"vectors":urlsVectors,"urls":urls})
"""
def getNearWebsites(urls,indexOfNearWebsites):
  websiteList=[]
  for i in range(len(indexOfNearWebsites[0])):
      websiteList.append(urls[indexOfNearWebsites[0][i]])
  return websiteList

def checkUrlInDb(url):
  try:
    query = "SELECT url, "
    for i in range(50):
      query += 'emb_d' + str(i)
      if(i != 49): query += ', '
    query += ' FROM global_data '
    conn = sqlite3.connect("server/database/web.db") 
    cur = conn.cursor()
    cursor = cur.execute(query)
    for row in cursor:
      cluster_no=row[0]
      new_url_vector=sToVec(row[1:])
    conn.close()
    return dict({"cluster_no":cluster_no,"new_url_vector":new_url_vector})
  except Exception as e:
      print("check url info err msg",e)
      return dict({"cluster_no":0,"new_url_vector":[]})

'''
def checkUrlInDb(url):
  try:
    conn = sqlite3.connect('server/database/web.db')
    cursor = conn.execute("SELECT cluster_no,embedding from data where url='"+str(url)+"'")
    for row in cursor:
      cluster_no=row[0]
      new_url_vector=sToVec(row[1])
    conn.close()
    return dict({"cluster_no":cluster_no,"new_url_vector":new_url_vector})
  except Exception as e:
      print("check url info err msg",e)
      return dict({"cluster_no":0,"new_url_vector":[]})  
'''
def giveUrlInfo(url):
  try:
      urlInfo = checkUrlInDb(url)
      if(len(urlInfo['new_url_vector'])!=0):
        print("url in databse")
        cluster_no = urlInfo['cluster_no']
        new_url_vector = urlInfo['new_url_vector'] 
      else:
        print("url not in database")
        content = preprocess(get_text_content(url))
        new_url_vector=sent_vectorizer(content,modelg)
        cluster_no=kmeans.predict([new_url_vector])[0]
        print("cluster",cluster_no)
      # print("cluster_no")
      # print(new_url_vector)  
      return dict({"cluster_no":cluster_no,"urlvector":new_url_vector})
  except Exception as e:
      print('giveUrlInfo error',e)
      return e
      

def finalFunction(url):
  try:
    urlInfo=giveUrlInfo(str(url))
    print("Url Info Done")
    ClusterNo = urlInfo['cluster_no']
    urlVector = urlInfo['urlvector']
    keywords = keyWordsOfCluster(ClusterNo)
    print("keywords",keywords)
    clusterVectors = getAllVecorsOfCluster(ClusterNo)
    
    vectors=clusterVectors['vectors']
    urls=clusterVectors['urls']
    print("Vectors of respective cluster ")
    indexOfNearWebsites = getIndexOfNearVectors(urlVector,vectors)
    print("Index pf websites")
    nearWebsites=getNearWebsites(urls,indexOfNearWebsites)
    print("near Websites")
    #print(websiteList)
    #print(keywordList)
    
    data_set = {"keywords": keywords, "websites": nearWebsites}

    json_dump = json.dumps(data_set)
    return data_set

  except Exception as e:
        print('ERROR_MSG',e)
        data_set={"keywords":[],"websites":[]}
        return data_set

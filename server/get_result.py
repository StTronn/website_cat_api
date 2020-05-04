from sklearn.neighbors import NearestNeighbors
from server import kmeans,X,labels,centroids,modelg,titles,l
from server.get_url import preprocess,get_text_content
from server.helper import sent_vectorizer
import json

def keyWordsOfCluster(clusterNo):
  neigh = NearestNeighbors(5)
  neigh.fit(X)
  index = neigh.kneighbors([centroids[clusterNo]], 5, return_distance=False)
  return index

def final_words(listoflist):
  l = [item for sublist in listoflist for item in sublist]
  wordfreq=[l.count(p) for p in l]
  mydict=dict(zip(l,wordfreq))
  newDict={k: v for k, v in sorted(mydict.items(), key=lambda item: item[1],reverse=True)}
  res = list(newDict.keys())[:10]
  return res

def getVectorOfUrl(content):
  try:
      return sent_vectorizer(content,modelg)
  except Exception as e:
      return e

def getIndexOfNearVectors(urlVector):
  try:
    neigh = NearestNeighbors(2, 0.4)
    neigh.fit(X)
    index = neigh.kneighbors([urlVector], 10, return_distance=False)
    return index
  except Exception as e:
    return e

def give_cluster(content):
  try:
      #print('URL name is :',url)
      # for key in final_dict.keys():
      #   for value in final_dict[key]:
      #     if(url==value):
      #       return key

      #print("line 1")
      new_url_vector=sent_vectorizer(content,modelg)
      #print("line 2")
      #print(kmeans.predict([new_url_vector])[0])
      return kmeans.predict([new_url_vector])[0]
  except Exception as e:
      return e
      # print('ERROR_MSG',e)

def finalFunction(url):
  try:
    # url = input("Enter Url:")
    # url = "https://choithramschool.com/"
    content=get_text_content(url)
    ClusterNo = give_cluster(content)
    print(ClusterNo)
    index = keyWordsOfCluster(ClusterNo)
    keywordList = []
    websiteList=[]
    urlVector = getVectorOfUrl(content)
    indexOfNearWebsites = getIndexOfNearVectors(urlVector)
    for i in range(len(indexOfNearWebsites[0])):
      websiteList.append(titles[indexOfNearWebsites[0][i]])
    for i in range(len(index[0])):
      keywordList.append(l[index[0][i]])
    keywordList =final_words(keywordList)
    #print(websiteList)
    #print(keywordList)
    data_set = {"keywords": keywordList, "websites": websiteList}

    json_dump = json.dumps(data_set)
    return data_set

  except Exception as e:
        #print('ERROR_MSG',e)
        data_set={"keywords":[],"websites":[]}
        return data_set

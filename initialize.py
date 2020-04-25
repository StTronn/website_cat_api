from gensim.models import Word2Vec,KeyedVectors
import pandas as pd
from helper import load_obj



EMBEDDING_FILE = 'GoogleNews-vectors-negative300.bin.gz'
modelg= KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True,limit=1000)

url='https://raw.githubusercontent.com/Pratikmehta1729/walkover/master/eng_sites_dataset_2.0_shuffled.csv'


#get titles,l,title_map
df = pd.read_csv(url)
l=[]
titles=[]
y=df.title.tolist()
x=df.text.tolist()

title_map={}
count=0
for title in y:
  title_map[title]=count
  titles.append(title)
  count+=1

for item in x:
    l.append(item.split())

sentences = l

kmeans=load_obj("kmeans")
X=load_obj("X")
labels=load_obj("labels")
centroids=load_obj("centroids")
final_dict=load_obj("final_dict")

print(kmeans)

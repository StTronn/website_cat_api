#kmeans object is kmeans_file 
#cluster is stored in sites_50_google.cluster
#for the function to work we will require the google model also 

def read_cluster(filename=''):
  with open('sites_50_google.cluster', 'rb') as cluster_file:
    cluster = pickle.load(cluster_file)
    return cluster

def load_kmeans():
  with open('kmeans_file', 'rb') as kmeans_file:
    kmeans = pickle.load(kmeans_file)
    return kmeans

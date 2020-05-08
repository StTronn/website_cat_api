import pandas as pd
import numpy as np
from flask import Flask
from server.helper import read_csv
from server.initialize import kmeans,labels,centroids,modelg,titles,l,X
from flask_cors import CORS, cross_origin
import json
import urllib.parse

print("in app")


print("loading search engine")
csv_url="websites_data.csv"
sites_df=pd.read_csv(csv_url)
y,z,centroid_no=read_csv(sites_df)
print("loaded search engine")

app = Flask(__name__)
from server.get_result import finalFunction
from server.search import search_by_query,search_by_domain
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

@app.route('/<path:url>')
@app.route('/')
@cross_origin()
def result_url(url=''):
    print(url)
    return finalFunction(url)

@app.route('/getclusterurl/<int:centroid_no>/page/<int:page_no>')
@app.route('/getclusterurl/<int:centroid_no>/')
@app.route('/getclusterurl/')
@cross_origin()
def get_cluster_url(centroid_no=-1,page_no=1):
    limit = len(sites_df)
    start = (page_no-1)*10
    end=page_no*10
    if centroid_no<0 or centroid_no >100:
        return json.dumps(sites_df[start:end][['rank','url']].to_dict('records'))
    cluster_df=sites_df[sites_df.centroid_no==centroid_no]
    return json.dumps(cluster_df[start:end][['rank','url']].to_dict('records'))

@app.route('/search/query/<q>')
@cross_origin()
def query_search(q):
    q=urllib.parse.unquote(q).split(" ")
    return json.dumps(search_by_query(q))

@app.route('/search/domain/<q>')
@cross_origin()
def domain_search(q):
    q=urllib.parse.unquote(q).split(" ")
    return json.dumps(search_by_domain(q))

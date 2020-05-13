import pandas as pd
import numpy as np
from flask import Flask
from server.helper import read_csv
from flask_cors import CORS, cross_origin
import server.initialize
import json
import urllib.parse
from server.helper import get_cluster_sites
print("in app")


print("loading search engine")
csv_url="websites_data.csv"
sites_df=pd.read_csv(csv_url)
y,z,centroid_no=read_csv(sites_df)
print("loaded search engine")

app = Flask(__name__)
from server.get_result import finalFunction
from server.search import search_by_query,search_by_domain,get_cluster_websites
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
    return json.dumps(get_cluster_sites(centroid_no))

@app.route('/search/query/<q>/clusterno/<int:cluster_no>')
@app.route('/search/query/<q>')
@cross_origin()
def query_search(q,cluster_no=-1):
    q=urllib.parse.unquote(q).split(" ")
    return json.dumps(search_by_query(q,cluster_no))

@app.route('/search/domain/<q>')
@cross_origin()
def domain_search(q):
    q=urllib.parse.unquote(q).split(" ")
    return json.dumps(search_by_domain(q))

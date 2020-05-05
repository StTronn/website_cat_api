import pandas as pd
from flask import Flask
from server.initialize import kmeans,X,labels,centroids,modelg,titles,l
from flask_cors import CORS, cross_origin
import json

print("in app")

csv_url="websites_data_csv.zip"
sites_df=pd.read_csv(csv_url)

app = Flask(__name__)
from server.get_result import finalFunction
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

@app.route('/<path:url>')
@app.route('/')
@cross_origin()
def result_url(url=''):
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


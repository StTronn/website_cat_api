from flask import Flask
from server.initialize import kmeans,X,labels,centroids,modelg,titles,l
from flask_cors import CORS, cross_origin

print("in app")

app = Flask(__name__)
from server.get_result import finalFunction
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

@app.route('/<path:url>')
@app.route('/')
@cross_origin()
def result_url(url=''):
    return finalFunction(url)



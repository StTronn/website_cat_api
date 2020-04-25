from flask import Flask
from initialize import kmeans,X,labels,centroids,modelg,titles,l
from get_result import finalFunction

app = Flask(__name__)

@app.route('/<path:url>')
@app.route('/')
def result_url(url=''):
    return finalFunction(url)


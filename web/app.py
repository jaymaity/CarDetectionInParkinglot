from flask import Flask, jsonify, render_template, request
from flask import request
from flask import session
from bs4 import BeautifulSoup
import urllib
import json
import imageprocess.imagesplit as imagesplit
import subprocess

app = Flask(__name__)

# set the secret key.
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getcurrent', methods=['GET', 'POST'])
def predict():
    with open('/home/jay/BigData/MLProj732/dl/static/data/Output.txt', 'r') as content_file:
        content = content_file.read()
    return content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

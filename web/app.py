import json
import os
from random import randint
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
# set the secret key.
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Reading values from config file
with open('../common/configs/live.config') as config_file:
    config = json.load(config_file)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getcurrent', methods=['GET', 'POST'])
def predict():

    filename, extension = config["OutputFileName"].split(".")
    maxno = len(os.listdir(config["OutputDataPath"]))
    fileno = randint(1, maxno)
    with open(config["OutputDataPath"] + filename+str(fileno)+"."+extension, 'r') as content_file:
        content = content_file.read()
    return content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

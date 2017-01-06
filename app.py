import json
import time

import requests
from flask import Flask, jsonify
from flask import render_template, request
from productData import ProductData

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

results = {}


@app.route('/index.html')
def home():
    return render_template("index.html")


@app.route('/answers.html', methods=['POST'])
def showResults():
    inputData = dict(request.form)
    jsonData = None
    for key in inputData:
        jsonData = json.loads(key)

    r = requests.get("http://api.prosperent.com/api/search?query=" + jsonData[
        'product'] + "&api_key=16b05be80ffaa9daf39618d7c3423028&sortBy=price&limit=10")
    data = json.loads(r.text)
    json_results = data['data']
    global results
    results = [ProductData(each_product['keyword'], each_product['merchant'], each_product['price'],
                           each_product['description'], each_product['affiliate_url'],
                           each_product['image_url']).__dict__ for
               each_product in json_results]
    return render_template("index.html")




@app.route('/results', methods=['GET'])
def parse():
    global results
    dataResult=jsonify(results)
    return dataResult

time.sleep(2)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

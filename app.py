import json
import time

import requests
from flask import Flask, jsonify
from flask import render_template, request
from productData import ProductData

app = Flask(__name__)

results = {}


@app.route('/index.html')
def home():
    return render_template("index.html")



@app.route('/index.html/search', methods=['POST'])
def parse():
    inputData = dict(request.form)
    jsonData = None
    for key in inputData:
        jsonData = json.loads(key)

    r = requests.get("http://api.prosperent.com/api/search?query=" + jsonData[
        'product'] + "&api_key=16b05be80ffaa9daf39618d7c3423028&sortBy=price")
    data = json.loads(r.text)
    json_results = data['data']

    global results
    results = [json.dumps(ProductData(each_product['keyword'], each_product['merchant'], each_product['price'],
                                      each_product['description'], each_product['affiliate_url'],
                                      each_product['image_url']).__dict__) for
               each_product in json_results]
    return render_template("answers.html")


@app.route('/answers.html', methods=['GET', 'POST'])
def showResults():
    global results

    return render_template("answers.html", userData=json.dumps(results))


time.sleep(2)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

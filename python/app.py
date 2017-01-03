from flask import Flask
import time,json
import urllib.request
import requests


from flask import render_template,redirect,url_for,request

import python.productData

app = Flask(__name__)



@app.route('/index.html')
def home():
    x=python.ProductData("","","","")
    return render_template("index.html")

@app.route('/search',methods=['POST'])
def getResults():
    inputData=dict(request.form)
    jsonData=None
    for key in inputData:
        jsonData=json.loads(key)

    r = requests.get("http://api.prosperent.com/api/search?query="+jsonData['product']+"&api_key=16b05be80ffaa9daf39618d7c3423028")
    data=json.loads(r.text)
    data1=data['data']
    return "done"

time.sleep(2)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

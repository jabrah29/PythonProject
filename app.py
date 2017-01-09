import io
import json
import time
import urllib

import googlemaps
from datetime import datetime
import requests
import tweepy
from flask import Flask, jsonify
from flask import render_template, request
from yelpProductData import ProductData
from yelpProductData import Deals
from yelp.client import Client
from GrouponProductData import GrouponProductData
from yelp.oauth1_authenticator import Oauth1Authenticator

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

results = []
dealsList=None


@app.route('/index.html')
def home():
    return render_template("index.html")




def login():
    with io.open('static/authentication.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
    return client



def grouponData(lat,lng):
    httpResult=urllib.request.urlopen("https://partner-api.groupon.com/deals.json?tsToken=US_AFF_0_201236_212556_0&lat="+lat+"&lng="+lng+"&filters=category:food-and-drink&offset=0&limit=10").read()

    json_obj = json.loads(httpResult.decode())
    groupon_data_list=[]
    for each in json_obj['deals']:
        groupon_data_list.append(GrouponProductData(each['title'],each['endAt'],
                                                    each['isSoldOut'],each['merchant']['name'],each['options'][0]['details'][0]['description'],
                                                    each['division']['lat'],each['division']['lng'],each['options'][0]['discount']['formattedAmount'],
                                                    each['options'][0]['price']['formattedAmount'],each['dealUrl']))
    return json_obj





@app.route('/answers.html', methods=['POST'])
def showResults():

    yelpClient=login()
    params = {
        'term': 'food',
        'radius_filter': '1500',
        'deals_filter': 'true',
        'cll' : request.form['lat']+","+request.form['lng']
    }

    grouponData(request.form['lat'], request.form['lng'])

    resultYelp=yelpClient.search('Chicago', **params)

    for key in resultYelp.businesses:
        dealsList = []
        for d in key.deals:
            dealsList.append(Deals(d.title, d.options[0].formatted_original_price, d.options[0].formatted_price, d.what_you_get ))
        if not key.location.address:
            addr="No Address Provided"
        else:
            addr=key.location.address[0]
            jsonList=jsonify(eqtls=[e.serialize() for e in dealsList])
        results.append(ProductData(key.name, key.rating,
                           key.distance, key.image_url,
                           jsonList, addr, key.location.coordinate.latitude,key.location.coordinate.longitude))


    send= eqtls=[e.serialize() for e in results]

    return send




@app.route('/results', methods=['GET'])
def parse():
    global results
    dataResult=jsonify(results)
    return dataResult

time.sleep(2)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

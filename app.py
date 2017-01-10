import io
import json
import time
import urllib

import googlemaps
from geopy.geocoders import Nominatim
from datetime import datetime
import requests
import tweepy
from flask import Flask, jsonify
from flask import render_template, request
from yelpProductData import ProductData
from yelpProductData import Deals
from SqootData import SqootData
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
    httpResult=urllib.request.urlopen("https://partner-api.groupon.com/deals.json?tsToken=US_AFF_0_201236_212556_0&lat="+lat+"&lng="+lng+"&filters=category:food-and-drink&offset=0&limit=50").read()

    json_obj = json.loads(httpResult.decode())
    groupon_data_list=[]
    for each in json_obj['deals']:
        groupon_data_list.append(GrouponProductData(each['title'],each['endAt'],
                                                    each['isSoldOut'],each['merchant']['name'],each['options'][0]['details'][0]['description'],
                                                    each['division']['lat'],each['division']['lng'],each['options'][0]['discount']['formattedAmount'],
                                                    each['options'][0]['price']['formattedAmount'],each['dealUrl']))
    return groupon_data_list





def getSqootData(lat,lng):
    url="http://api.sqoot.com/v2/deals?api_key=ym05r0&location="+lat+","+lng+"&category_slugs=restaurants&per_page=50"
    httpResult=urllib.request.urlopen(url.replace("'","")).read()
    json_obj = json.loads(httpResult.decode())
    sqoot_data_list=[]
    for each in json_obj['deals']:
        sqoot_data_list.append(SqootData(each['deal']['title'],each['deal']['merchant']['address'],
                                                    each['deal']['merchant']['phone_number'],each['deal']['image_url'],each['deal']['title'],
                                                    each['deal']['expires_at'],each['deal']['value'],each['deal']['price'],
                                                    each['deal']['fine_print'],each['deal']['url'], each['deal']['merchant']['latitude'],each['deal']['merchant']['longitude']))


    return sqoot_data_list




@app.route('/answers.html', methods=['POST'])
def showResults():

    yelpClient=login()
    params = {}
    params["term"] = "restaurant"
    params["cll"] = request.form['lat']+","+request.form['lng']
    params["radius_filter"] = "2000"
    params["deals_filter"] = 'true'

    geolocator = Nominatim()
    location = geolocator.reverse(request.form['lat']+','+request.form['lng'])
    grouponList=grouponData(request.form['lat'], request.form['lng'])
    sqootList=getSqootData(request.form['lat'], request.form['lng'])

    resultYelp=yelpClient.search('Chicago', **params)
    resultYelp2=yelpClient.search('Chicago',**params)

    y1=parseYelpResult(resultYelp)
    y2=parseYelpResult(resultYelp2)




    a_names = {each.store_name for each in grouponList}
    b_names = {each.name for each in y1}
    b1_names ={each.name for each in y2}
    combined_list=[]
    for b,b1 in zip(b1_names,b_names):
        combined_list.append(b)
        combined_list.append(b1)


    answer=[item for item in combined_list if item in a_names]
    send = eqtls=[e.serialize() for e in results]

    return send






def parseYelpResult(list):
    methodResults = []
    for key in list.businesses:
        dealsList = []

        for d in key.deals:
            dealsList.append(Deals(d.title, d.options[0].formatted_original_price, d.options[0].formatted_price, d.what_you_get ))
        if not key.location.address:
            addr="No Address Provided"
        else:
            addr=key.location.address[0]
            jsonList=jsonify(eqtls=[e.serialize() for e in dealsList])
        methodResults.append(ProductData(key.name, key.rating,
                           key.distance, key.image_url,
                           jsonList, addr, key.location.coordinate.latitude,key.location.coordinate.longitude))

    return methodResults

@app.route('/results', methods=['GET'])
def parse():
    global results
    dataResult=jsonify(results)
    return dataResult

time.sleep(2)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

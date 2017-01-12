import io
import json
import time
import urllib

import foursquare
import googlemaps
import itertools
import timeit
from operator import itemgetter
from geopy.geocoders import Nominatim

import tweepy
from flask import Flask, jsonify
from flask import render_template, request
from multiprocessing import Process

from yelpProductData import ProductData
from yelpProductData import Deals
from SqootData import SqootData
from yelp.client import Client
from GrouponProductData import GrouponProductData
from yelp.oauth1_authenticator import Oauth1Authenticator

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

results = []
grouponList=[]
ylist=[]
sqootList=[]
dealsList = None


@app.route('/index.html')
def home():
    return render_template("index.html")


def login():
    with io.open('static/authentication.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
    return client


def grouponData(lat, lng):
    httpResult = urllib.request.urlopen(
        "https://partner-api.groupon.com/deals.json?tsToken=US_AFF_0_201236_212556_0&lat=" + lat + "&lng=" + lng + "&filters=category:food-and-drink&offset=0&radius=5&limit=50").read()

    json_obj = json.loads(httpResult.decode())
    groupon_data_list = []
    for each in json_obj['deals']:
        groupon_data_list.append(GrouponProductData(each['title'], each['options'][0]['expiresAt'],
                                                    each['isSoldOut'], each['merchant']['name'],
                                                    each['options'][0]['details'][0]['description'],
                                                    each['division']['lat'], each['division']['lng'],
                                                    each['options'][0]['discount']['formattedAmount'],
                                                    each['options'][0]['price']['formattedAmount'], each['dealUrl'],
                                                    each['options'][0]['price']['amount'],
                                                    each['options'][0]['discount']['amount'],each['uuid']))
    return groupon_data_list


def getSqootData(lat, lng):
    url = "http://api.sqoot.com/v2/deals?api_key=ym05r0&location=" + lat + "," + lng + "&radius=5&category_slugs=restaurants&per_page=50"
    httpResult = urllib.request.urlopen(url.replace("'", "")).read()
    json_obj = json.loads(httpResult.decode())
    sqoot_data_list = []
    for each in json_obj['deals']:
        sqoot_data_list.append(SqootData(each['deal']['merchant']['name'], each['deal']['merchant']['address'],
                                         each['deal']['merchant']['phone_number'], each['deal']['image_url'],
                                         each['deal']['title'],
                                         each['deal']['expires_at'], each['deal']['value'], each['deal']['price'],
                                         each['deal']['fine_print'], each['deal']['url'],
                                         each['deal']['merchant']['latitude'], each['deal']['merchant']['longitude'],each['deal']['id']))

    return sqoot_data_list



@app.route('/answers.html', methods=['POST'])
def showResults():
    start = timeit.default_timer()

    yelpClient = login()
    params = {}
    params["term"] = "dinner"
    params["cll"] = request.form['lat'] + "," + request.form['lng']
    params["radius_filter"] = "2000"
    params["deals_filter"] = 'true'
    params['radius_filter']='8049'



    geolocator = Nominatim()
    location = geolocator.reverse(request.form['lat'] + ',' + request.form['lng'])
    global grouponList
    grouponList = grouponData(request.form['lat'], request.form['lng'])
    global sqootList
    sqootList = getSqootData(request.form['lat'], request.form['lng'])

    resultYelp = yelpClient.search('Chicago', **params)

    global ylist
    ylist=parseYelpResult(resultYelp)



    price_margins=parsePrices(ylist, grouponList, sqootList)
    combinedList=[price_margins[0],price_margins[1],price_margins[2]]
    fullList=[y for x in combinedList for y in x]





    stop = timeit.default_timer()

    print(stop - start)
    a_names = {each.store_name for each in grouponList}
    b_names = {each.name for each in ylist}
    c_names = {each.store_name for each in sqootList}
    combined_list = []

    common = list((set(a_names) | set(b_names)) & set(c_names))

    send = eqtls = [e.serialize() for e in results]

    return send


def parsePrices(yelpList, grouponList, sqootList):
    minPriceYelp = tuple([ (yelp.deals[0].orig_price_calculation, yelp.deals[0].dis_price_calculation,yelp.id) for yelp in yelpList ])
    minPriceGroup = tuple([(groupon.calculatedPrice, groupon.calculatedDiscount,groupon.id) for groupon in grouponList ])
    minPriceSqoot =  tuple([(sqoot.orig_price, sqoot.discount_price,sqoot.id) for sqoot in sqootList ])

    yelp_difference=[]
    groupon_difference=[]
    sqoot_difference=[]
    yelp_difference=calculate_difference_and_max(minPriceYelp)
    groupon_difference=calculate_difference_and_max(minPriceGroup)
    sqoot_difference=calculate_difference_and_max(minPriceSqoot)
    return (yelp_difference,groupon_difference,sqoot_difference)




def calculate_difference_and_max(list):
    send_list=[]
    id_list=[]

    for key in list:
        send_list.append(key[0]-key[1])
        id_list.append(key[2])
    diction=dict(zip(id_list,send_list))
    return sorted(diction.items(), key=lambda x:x[1])




def parseYelpResult(list):
    methodResults = []
    for key in list.businesses:
        dealsList = []
        id_temp=''
        for d in key.deals:
            id_temp=d.id
            dealsList.append(
                Deals(d.title, d.options[0].formatted_original_price, d.options[0].formatted_price, d.what_you_get,
                      d.options[0].original_price, d.options[0].price))
        if not key.location.address:
            addr = "No Address Provided"
        else:
            addr = key.location.address[0]
        methodResults.append(ProductData(key.name, key.rating,
                                         key.distance, key.image_url,
                                         dealsList, addr, key.location.coordinate.latitude,
                                         key.location.coordinate.longitude,id_temp))

    return methodResults


@app.route('/results', methods=['GET'])
def parse():
    global results
    dataResult = jsonify(results)
    return dataResult


time.sleep(2)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)


class ValHolder(object):
    firstval = None
    secondVal = None
    id=None

    def __init__(self, f, s, id):
        self.firstval = f
        self.secondVal = s
        self.id=id
